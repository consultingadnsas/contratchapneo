from django.urls import path
from .views import (
    CartDetailView,
    CartAddItemView,
    CartAddPack,
    CartRemoveItemView,
    CartClearView,
    CartItemUpdateView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    OrderCancelView,
    OrderDownloadView,
    ApplyCouponView,
    RemoveCouponView
)

urlpatterns = [
    # Panier
    path('cart/',                    CartDetailView.as_view(),    name='cart-detail'),
    path('cart/add/',                CartAddItemView.as_view(),   name='cart-add'),
    path('cart/pack/add/',            CartAddPack.as_view(),       name='add-pack'),
    path('cart/update/<uuid:contrat_id>/', CartItemUpdateView.as_view(), name='cart-update-item'),
    path('cart/remove/<uuid:item_id>/', CartRemoveItemView.as_view(), name='cart-remove'),
    path('cart/clear/',              CartClearView.as_view(),     name='cart-clear'),
    path('cart/checkout/',           CheckoutView.as_view(),      name='cart-checkout'),

    # Commandes
    path('orders/',                        OrderListView.as_view(),   name='order-list'),
    path('orders/<uuid:order_id>/',        OrderDetailView.as_view(), name='order-detail'),
    path('orders/<uuid:order_id>/download/', OrderDownloadView.as_view(), name='order-download'),
    path('orders/<uuid:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),

    # Coupon
    path('cart/apply-coupon/', ApplyCouponView.as_view(), name='apply-coupon'),
    path('cart/remove-coupon/', RemoveCouponView.as_view(), name='remove-coupon'),
]