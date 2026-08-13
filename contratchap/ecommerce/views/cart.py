from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F

from ..models import Cart, CartItem, Order, OrderItem, GuestInfo, Coupon
from ..serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    AddToCartSerializer,
    CheckoutSerializer,
)
from ..helpers import (get_or_create_cart, set_cart_cookie_if_needed)
from contrat.models import Contrat, CustomedContract, Pack, ContractRevision
from pro.models import LegalProfessional

from contrat.utils import fill_docx_template, convert_docx_to_pdf, send_documents_by_email_async

# ─────────────────────────────────────────
# CART VIEWS
# ─────────────────────────────────────────

class AdminCartPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ApplyCouponView(APIView):
    """
    POST /cart/apply-coupon/
    Applique un code promo au panier de l'utilisateur.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        cart = get_or_create_cart(request)
        code = request.data.get('code')

        if not code:
            return Response(
                {"error": "Veuillez fournir un code promo."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            coupon = Coupon.objects.get(code__iexact=code)
            
            # 🚨 VÉRIFICATION STRICTE : actif, dates et nombre d'utilisations
            if not coupon.is_valid():
                return Response(
                    {"error": "Ce code promo est invalide, expiré ou a atteint sa limite d'utilisation."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Coupon.DoesNotExist:
            return Response(
                {"error": "Ce code promo n'existe pas."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # On applique le coupon au panier
        cart.coupon = coupon
        cart.save()

        # On renvoie le panier mis à jour (avec les nouveaux sous-totaux !)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveCouponView(APIView):
    """
    POST /cart/remove-coupon/
    Retire le code promo du panier.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        cart = get_or_create_cart(request)
        
        # On vide le champ coupon
        cart.coupon = None
        cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartDetailView(APIView):
    """
    GET /cart/
    Retourne le panier courant avec ses lignes.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

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
    authentication_classes = []

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
        customed_contract_id = serializer.validated_data.get('customed_contract')
        pack_id = serializer.validated_data.get('pack_id') # et non get('pack')
        contract_revision_id = serializer.validated_data.get('contract_revision_id')
        quantity   = serializer.validated_data.get('quantity', 1)

        # Vérification de sécurité
        if not contrat_id and not pro_id and not customed_contract_id and not pack_id and not contract_revision_id:
             return Response(
                {'errors': 'Vous devez fournir soit un contrat_id, soit un pro_id, soit un customed_contract, soit un pack_id, soit un contract_revision_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚖️ LOGIQUE HYBRIDE : CONTRAT OU PRO OU CONTRAT SUR MESURE
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

        elif customed_contract_id:
            customed_contract = get_object_or_404(CustomedContract, id=customed_contract_id)
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                customed_contract=customed_contract,
                defaults={
                    'quantity'  : quantity,
                    'unit_price': customed_contract.price,
                }
            )
            if not created:
                item.quantity += quantity
                item.save()

        elif pack_id:
            # J'utilise une variable 'pack_obj' pour éviter la confusion
            pack_obj = get_object_or_404(Pack, id=pack_id) 
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                packs=pack_obj, # 🚨 CORRECTION : "packs" (avec un 's'), car c'est le vrai nom de ton champ dans ton Model !
                defaults={
                    'quantity'  : quantity,
                    'unit_price': pack_obj.prix,
                }
            )
            if not created:
                item.quantity += quantity
                item.save()

        elif contract_revision_id:
            revision_request = get_object_or_404(ContractRevision, id=contract_revision_id)
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                contract_revision=revision_request,
                defaults={
                    'quantity': quantity,
                    'unit_price': revision_request.price,
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

class CartAddPack(APIView):
    """ 
    POST /cart/pack/add/ 
    Ajoute un pack au panier (Connexion obligatoire !)
    """
    # 🔒 C'est cette ligne qui fait toute la magie : DRF bloquera 
    # automatiquement avec une erreur 401 si l'utilisateur n'est pas connecté.
    permission_classes = [IsAuthenticated]
    
    # ⚠️ Enlève `authentication_classes = []` pour que DRF puisse 
    # utiliser tes tokens JWT ou tes cookies de session pour identifier l'utilisateur !

    def post(self, request):
        # 1. On récupère l'ID du pack et la quantité depuis le corps de la requête
        pack_id = request.data.get('pack_id')
        quantity = int(request.data.get('quantity', 1))

        if not pack_id:
            return Response(
                {'errors': 'Vous devez fournir un pack_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. On récupère le pack depuis la base de données
        pack_obj = get_object_or_404(Pack, id=pack_id)

        # 3. On récupère le panier (qui sera forcément lié au `request.user` grâce à IsAuthenticated)
        cart = get_or_create_cart(request)

        # 4. On ajoute le pack au panier (ou on augmente la quantité s'il y est déjà)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            packs=pack_obj, # On utilise bien 'packs' (avec un 's') comme vu précédemment
            defaults={
                'quantity': quantity,
                'unit_price': pack_obj.prix,
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        # 5. On renvoie le panier mis à jour
        response = Response(
            {
                'data': CartSerializer(cart).data,
                'message': 'Pack ajouté au panier avec succès !'
            },
            status=status.HTTP_200_OK
        )
        
        # 6. Optionnel mais recommandé, on maintient la logique de cookie
        return set_cart_cookie_if_needed(request, response)

class CartItemUpdateView(APIView):
    """
        PATCH /cart/update/<uuid:contrat_id>/
        Met à jour la quantité d'un contrat spécifique dans le panier.
    """
    # AllowAny car les utilisateurs invités (sessions) peuvent aussi modifier leur panier
    permission_classes = [AllowAny]
    authentication_classes = []

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
    authentication_classes = []

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
    authentication_classes = []

    def delete(self, request):
        cart = get_or_create_cart(request)
        cart.clear()

        response = Response(
            {'message': 'Panier vidé.'},
            status=status.HTTP_200_OK
        )
        return set_cart_cookie_if_needed(request, response)

# =========================================================
# 1. Admin Cart Management
# =========================================================

class AdminCartView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer
    pagination_class = AdminCartPagination