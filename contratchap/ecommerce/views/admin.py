from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.utils import timezone
from datetime import timedelta

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
from django.shortcuts import get_object_or_404

class AdminPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 
    max_page_size = 100

class AdminCartView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer
    pagination_class = AdminPagination

class AdminOrderView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    pagination_class = AdminPagination

    def get_queryset(self):
        # 1. On récupère toutes les commandes, triées par date (de la plus récente à la plus ancienne)
        queryset = Order.objects.all().order_by('-created_at')
        
        # 2. On vérifie si l'URL contient le paramètre ?abandoned=true
        is_abandoned = self.request.query_params.get('abandoned')
        
        if is_abandoned == 'true':
            # On calcule l'heure exacte qu'il était il y a 1 heure
            time_threshold = timezone.now() - timedelta(hours=1)
            
            # 3. On filtre : Uniquement les commandes en attente ("pending") 
            #    ET créées avant la limite d'une heure (lte = less than or equal)
            queryset = queryset.filter(
                status='pending',
                created_at__lte=time_threshold
            )
            
        return queryset

# ==========================================
# 1. LISTER LES COUPONS (Ton code)
# ==========================================
class AdminCouponList(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Coupon.objects.all().order_by('-id')
    serializer_class = CouponSerializer
    pagination_class = AdminPagination

# ==========================================
# 2. CRÉER UN COUPON (Ton code, renommé)
# ==========================================
class AdminCouponCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            serializer = CouponSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Coupon créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        except Exception:
            return Response(
                {"error": "Une erreur liée au serveur est survenue, réessayez plus tard."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ==========================================
# 3. DÉTAIL, MODIFICATION & SUPPRESSION (Le nouveau code)
# ==========================================
class AdminCouponDetailView(APIView):
    """
    Nécessite l'ID du coupon dans l'URL (ex: /admin/coupons/1/)
    """
    permission_classes = [IsAdminUser]

    # READ : Récupérer les infos d'un seul code promo
    def get(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        serializer = CouponSerializer(coupon)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # UPDATE : Modifier un code promo existant
    def put(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        try:
            # partial=True permet de faire des modifications partielles (ex: juste changer la date)
            serializer = CouponSerializer(coupon, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Code promo mis à jour !"}, 
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Une erreur est survenue lors de la modification."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # DELETE : Supprimer un code promo
    def delete(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        try:
            coupon.delete()
            return Response(
                {"message": "Code promo supprimé avec succès."}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(
                {"error": "Impossible de supprimer ce code promo pour le moment."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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