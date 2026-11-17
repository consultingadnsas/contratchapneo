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
from ..helpers import (get_or_create_cart, set_cart_cookie_if_needed, create_order_from_cart)
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
        guest = None
        if not request.user.is_authenticated:
            guest_data = validated_data['guest']
            guest = GuestInfo.objects.create(
                email=guest_data.get('email'),
                full_name=guest_data.get('full_name'),
                phone_number=guest_data.get('phone_number', '')
            )

        return create_order_from_cart(request, cart, guest=guest)