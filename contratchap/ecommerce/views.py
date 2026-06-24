import stripe
from django.conf import settings
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
    AddToCartSerializer,
    CheckoutSerializer,
)
from .helpers import (get_or_create_cart, set_cart_cookie_if_needed)
from contrat.models import Contrat
from pro.models import LegalProfessional

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    Ajoute un contrat ou un professionnel au panier.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart       = get_or_create_cart(request)
        
        # 🚨 CORRECTION ICI : On utilise .get() pour éviter le KeyError
        contrat_id = serializer.validated_data.get('contrat_id')
        pro_id     = serializer.validated_data.get('pro_id')
        quantity   = serializer.validated_data.get('quantity', 1)

        # Vérification de sécurité
        if not contrat_id and not pro_id:
             return Response(
                {'errors': 'Vous devez fournir soit un contrat_id, soit un pro_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚖️ LOGIQUE HYBRIDE : CONTRAT OU PRO
        if contrat_id:
            contrat = get_object_or_404(Contrat, id=contrat_id)
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
                
        elif pro_id:
            pro = get_object_or_404(LegalProfessional, id=pro_id)
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                pro=pro,
                defaults={
                    'quantity'  : quantity,
                    'unit_price': pro.prix,
                }
            )
            if not created:
                item.quantity += quantity
                item.save()

        # Construction de la réponse identique à ton code
        response = Response(
            {
                'data'   : CartSerializer(cart).data,
                'message': 'Élément ajouté au panier.'
            },
            status=status.HTTP_200_OK
        )
        
        # On conserve ta logique de cookies hyper importante !
        return set_cart_cookie_if_needed(request, response)

class CartItemUpdateView(APIView):
    """
    PATCH /cart/update/<uuid:contrat_id>/
    Met à jour la quantité d'un contrat spécifique dans le panier.
    """
    # AllowAny car les utilisateurs invités (sessions) peuvent aussi modifier leur panier
    permission_classes = [AllowAny]

    def patch(self, request, contrat_id):
        # 1. On récupère le panier de l'utilisateur (ou de la session)
        cart = get_or_create_cart(request)

        # 2. On cherche la ligne du panier correspondante
        try:
            cart_item = CartItem.objects.get(cart=cart, contrat_id=contrat_id)
        except CartItem.DoesNotExist:
            return Response(
                {'message': 'Ce contrat n\'est pas dans votre panier.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. On extrait et valide la nouvelle quantité
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response(
                {'message': 'La quantité est requise.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                # Si la quantité est 0, l'idéal est de dire au front d'utiliser la route DELETE
                # ou tu pourrais choisir de supprimer l'item ici directement (cart_item.delete())
                return Response(
                    {'message': 'La quantité doit être supérieure à zéro.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'message': 'La quantité doit être un nombre entier valide.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. On met à jour et on sauvegarde
        cart_item.quantity = quantity
        cart_item.save()

        # 5. On renvoie l'état complet du panier mis à jour (comme attendu par ton store Pinia)
        serializer = CartSerializer(cart)
        
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        # Astuce : Si c'est un invité, s'assurer que le cookie de session suit bien
        # set_cart_cookie_if_needed(request, response) -> Décommente si tu utilises ce helper pour la réponse
        
        return response

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

        # 1️⃣ Création du GuestInfo si invité
        guest = None
        if not request.user.is_authenticated:
            guest_data = validated_data['guest']
            guest = GuestInfo.objects.create(
                email       =guest_data.get('email'),
                full_name   =guest_data.get('full_name'),
                phone_number=guest_data.get('phone_number', '') 
            )

        # Snapshot du total depuis le panier
        total = cart.get_total()

        # Création de la commande
        order = Order.objects.create(
            user        =request.user if request.user.is_authenticated else None,
            guest       =guest,
            total_amount=total,
        )

        # Création des lignes de commande
        order_items = []
        
        for item in cart.items.select_related('contrat', 'pro'):
            
            # 2️⃣ On prépare les deux variables séparément
            c_title = None
            p_name = None
            
            if item.contrat:
                # CORRECTION : Le champ s'appelle 'titre' et non 'title'
                c_title = item.contrat.title
            elif item.pro:
                # CORRECTION : Utilisation de get_title_display() si c'est un champ choices, 
                # sinon on récupère simplement l'attribut 'title'.
                pro_title = item.pro.get_title_display() if hasattr(item.pro, 'get_title_display') else getattr(item.pro, 'title', '')
                p_name = f"{item.pro.first_name} {item.pro.last_name} - {pro_title}"

            # 3️⃣ On insère chaque info dans SA propre colonne
            order_items.append(
                OrderItem(
                    order        =order,
                    contrat      =item.contrat,
                    pro          =item.pro,  
                    contrat_title=c_title,  
                    pro_name     =p_name,   
                    unit_price   =item.unit_price,
                    quantity     =item.quantity,
                )
            )
            
        # Enregistrement en masse
        OrderItem.objects.bulk_create(order_items)

        # 4️⃣ CORRECTION : On vide le panier une fois la commande passée !
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