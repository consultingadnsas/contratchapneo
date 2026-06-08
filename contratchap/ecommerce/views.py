from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Cart, CartItem, Order, OrderItem, GuestInfo
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    CheckoutSerializer,
)
from contrat.models import Contrat


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def get_or_create_cart(request):
    """
    Retourne le panier existant ou en crée un nouveau.
    - User connecté  → panier lié au user
    - Invité         → panier lié à la session Django
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    # Crée la session si elle n'existe pas encore
    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
    return cart

def set_cart_cookie_if_needed(request, response):
    """
    Helper pour attacher le cookie 'cart_session_id' à la réponse 
    si un nouveau panier a été créé pour un invité.
    """
    if hasattr(request, '_new_cart_session_id'):
        response.set_cookie(
            key='cart_session_id',
            value=request._new_cart_session_id,
            httponly=True,  # Sécurisé contre les failles XSS
            max_age=30 * 24 * 60 * 60,  # Expire dans 30 jours
            samesite='Lax'
        )
    return response

# ─────────────────────────────────────────
# CART VIEWS
# ─────────────────────────────────────────

class CartDetailView(APIView):
    """
    GET /cart/
    Retourne le panier courant avec ses lignes.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return set_cart_cookie_if_needed(request, response)


class CartAddItemView(APIView):
    """
    POST /cart/add/
    Ajoute un contrat au panier.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart       = get_or_create_cart(request)
        contrat_id = serializer.validated_data['contrat_id']
        quantity   = serializer.validated_data.get('quantity', 1)
        contrat    = get_object_or_404(Contrat, id=contrat_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            contrat=contrat,
            defaults={
                'quantity'  : quantity,
                'unit_price': contrat.prix,
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        response = Response(
            {
                'data'   : CartSerializer(cart).data,
                'message': 'Contrat ajouté au panier.'
            },
            status=status.HTTP_200_OK
        )
        return set_cart_cookie_if_needed(request, response)


class CartRemoveItemView(APIView):
    """
    DELETE /cart/remove/<item_id>/
    Supprime une ligne du panier.
    """
    permission_classes = [AllowAny]

    def delete(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        response = Response(
            {
                'data'   : CartSerializer(cart).data,
                'message': 'Article retiré du panier.'
            },
            status=status.HTTP_200_OK
        )
        return set_cart_cookie_if_needed(request, response)


class CartClearView(APIView):
    """
    DELETE /cart/clear/
    Vide entièrement le panier.
    """
    permission_classes = [AllowAny]

    def delete(self, request):
        cart = get_or_create_cart(request)
        cart.clear()

        response = Response(
            {'message': 'Panier vidé.'},
            status=status.HTTP_200_OK
        )
        return set_cart_cookie_if_needed(request, response)

# ─────────────────────────────────────────
# CHECKOUT VIEW
# ─────────────────────────────────────────

class CheckoutView(APIView):
    """
    POST /cart/checkout/
    Transforme le panier en commande.

    Body (user connecté)  : {}
    Body (invité)         : { "guest": { "email": "...", "full_name": "..." } }

    Étapes :
    1. Valide le panier (non vide)
    2. Valide les infos guest si nécessaire
    3. Crée Order + OrderItems dans une transaction atomique
    4. Vide le panier
    5. Retourne la commande créée
    """
    permission_classes = [AllowAny]

    def post(self, request):
        cart = get_or_create_cart(request)

        # 1. Panier vide ?
        if not cart.items.exists():
            return Response(
                {'message': 'Votre panier est vide.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Validation des données (guest obligatoire si non connecté)
        serializer = CheckoutSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Création atomique de la commande
        try:
            with transaction.atomic():
                order = self._create_order(request, cart, serializer.validated_data)
        except Exception as e:
            return Response(
                {
                    'message': 'Erreur lors de la création de la commande.',
                    'error'  : str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(
            {
                'data'   : OrderSerializer(order).data,
                'message': 'Commande créée avec succès.'
            },
            status=status.HTTP_201_CREATED
        )
        return set_cart_cookie_if_needed(request, response)

    def _create_order(self, request, cart, validated_data):
        """Logique de création isolée — appelée dans la transaction atomique."""

        # Création du GuestInfo si invité
        guest = None
        if not request.user.is_authenticated:
            guest_data = validated_data['guest']
            guest = GuestInfo.objects.create(
                email    =guest_data['email'],
                full_name=guest_data['full_name'],
            )

        # Snapshot du total depuis le panier
        total = cart.get_total()

        # Création de la commande
        order = Order.objects.create(
            user        =request.user if request.user.is_authenticated else None,
            guest       =guest,
            total_amount=total,
        )

        # Création des lignes de commande depuis les lignes du panier
        order_items = [
            OrderItem(
                order        =order,
                contrat      =item.contrat,
                contrat_title=item.contrat.title,
                unit_price   =item.unit_price,
                quantity     =item.quantity,
            )
            for item in cart.items.select_related('contrat')
        ]
        OrderItem.objects.bulk_create(order_items)

        # Vidage du panier
        cart.clear()

        return order


# ─────────────────────────────────────────
# ORDER VIEWS
# ─────────────────────────────────────────

class OrderListView(APIView):
    """
    GET /orders/
    Liste les commandes de l'utilisateur connecté.
    Non accessible aux invités (ils n'ont pas de compte).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            user=request.user
        ).prefetch_related('order_items')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """
    GET /orders/<order_id>/
    Détail d'une commande.
    Accessible au user connecté propriétaire OU à l'invité via son email.
    """
    permission_classes = [AllowAny]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.prefetch_related('order_items'),
            id=order_id
        )

        # Vérification d'accès
        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé à cette commande.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _can_access(self, request, order):
        """
        User connecté → doit être le propriétaire.
        Invité        → doit fournir son email en query param.
        """
        if request.user.is_authenticated:
            return order.user == request.user

        # Invité : GET /orders/<id>/?email=john@example.com
        email = request.query_params.get('email', '').lower().strip()
        return (
            order.guest is not None and
            order.guest.email == email
        )


class OrderCancelView(APIView):
    """
    POST /orders/<order_id>/cancel/
    Annule une commande en statut 'pending'.
    """
    permission_classes = [AllowAny]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not order.can_be_cancelled():
            return Response(
                {'message': f'Une commande avec le statut « {order.get_status_display()} » ne peut pas être annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = Order.Status.CANCELLED
        order.save()

        return Response(
            {
                'data'   : OrderSerializer(order).data,
                'message': 'Commande annulée avec succès.'
            },
            status=status.HTTP_200_OK
        )

    def _can_access(self, request, order):
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return (
            order.guest is not None and
            order.guest.email == email
        )