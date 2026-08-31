import tempfile
import zipfile
import io
import os
from PIL.DdsImagePlugin import item
from PIL.Image import item
from django.http import FileResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F

from ..models import CartItem, Order, OrderItem, GuestInfo, Coupon
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

        # 1. Calcul des montants avec et sans réduction
        subtotal = cart.get_total()
        final_total = cart.get_total_with_discount()
        discount = subtotal - final_total

        # 2. Création de la commande avec le snapshot complet du coupon
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            guest=guest,
            total_amount=final_total,
            coupon=cart.coupon,           # 👈 On lie le coupon utilisé
            discount_amount=discount,     # 👈 On fige l'économie réalisée
        )

        if order.coupon:
            Coupon.objects.filter(id=order.coupon.id).update(used_count=F('used_count') + 1)

        order_items = []
        
        # NOUVEAU : On ajoute 'packs' au select_related pour optimiser la DB
        for item in cart.items.select_related('contrat', 'pro', 'customed_contract', 'packs', 'contract_revision'):
            
            c_title = None
            p_name = None
            customized_name = None
            pack_title = None
            contract_revision = None
            revision_subject = None
            
            if item.contrat:
                c_title = item.contrat.title
            elif item.pro:
                pro_title = item.pro.get_title_display() if hasattr(item.pro, 'get_title_display') else getattr(item.pro, 'title', '')
                p_name = f"{item.pro.first_name} {item.pro.last_name} - {pro_title}"
            elif item.customed_contract:
                customized_name = item.customed_contract.subject or f"Contrat sur mesure #{item.customed_contract.id}"
            elif item.packs:
                pack_title = item.packs.title
            elif item.contract_revision:
                contract_revision = item.contract_revision
                revision_subject = item.contract_revision.subject or f"Révision #{item.contract_revision.id}"

            order_items.append(
                OrderItem(
                    order=order,
                    contrat=item.contrat,
                    pro=item.pro,
                    contrat_customed=item.customed_contract,
                    pack=item.packs,
                    contrat_title=c_title,
                    customised_contract=customized_name,
                    contract_revision=contract_revision,
                    pro_name=p_name,
                    pack_title=pack_title,
                    revision_subject=revision_subject,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                )
            )
            
        OrderItem.objects.bulk_create(order_items)
        cart.clear()

        return order