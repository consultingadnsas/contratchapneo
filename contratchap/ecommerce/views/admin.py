from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from ..models import Cart, CartItem, Order, OrderItem, Coupon
from ..serializers import (
    CartSerializer, 
    CartItemSerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    GuestInfoSerializer,
    CouponSerializer,
    AccountingOrderSerializer  # 👈 NOUVEAU : N'oublie pas d'importer le sérialiseur de compta
)

class AdminPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100

class AdminCartView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer
    pagination_class = AdminPagination

class AdminOrderView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    pagination_class = AdminPagination

class AdminCouponList(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all().order_by('-id')
    serializer_class = CouponSerializer
    pagination_class = AdminPagination

class AdminCouponView(APIView):
    def get(self, request):
        pass

# ─────────────────────────────────────────
# VUE DE COMPTABILITÉ
# ─────────────────────────────────────────

class AdminAccountingView(ListAPIView):
    """
    Vue dédiée au tableau de bord financier et aux exports comptables.
    Utilise un sérialiseur allégé avec des données "plates" et lisibles.
    """
    permission_classes = [IsAdminUser]
    
    # 💡 Astuce Contratchap : Pour la compta, il est souvent plus logique 
    # de ne récupérer que les commandes effectivement PAYÉES (status='paid').
    # Si tu veux vraiment toutes les commandes, remplace `.filter(status='paid')` par `.all()`
    queryset = Order.objects.filter(status='paid').order_by('-created_at')
    
    serializer_class = AccountingOrderSerializer
    pagination_class = AdminPagination