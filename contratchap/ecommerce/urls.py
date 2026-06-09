from django.urls import path
from .views import (
    CartDetailView,
    CartAddItemView,
    CartRemoveItemView,
    CartClearView,
    CheckoutView,
    OrderListView,
    OrderDetailView,
    OrderCancelView,
)

urlpatterns = [
    # Panier
    path('cart/',                    CartDetailView.as_view(),    name='cart-detail'),
    path('cart/add/',                CartAddItemView.as_view(),   name='cart-add'),
    path('cart/remove/<uuid:item_id>/', CartRemoveItemView.as_view(), name='cart-remove'),
    path('cart/clear/',              CartClearView.as_view(),     name='cart-clear'),
    path('cart/checkout/',           CheckoutView.as_view(),      name='cart-checkout'),

    # Commandes
    path('orders/',                        OrderListView.as_view(),   name='order-list'),
    path('orders/<uuid:order_id>/',        OrderDetailView.as_view(), name='order-detail'),
    path('orders/<uuid:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]