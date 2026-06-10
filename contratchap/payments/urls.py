from django.urls import path
from .views import PaymentInitiateView, PaymentSimulateView, PaymentWebhookView

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('simulate/', PaymentSimulateView.as_view(), name='payment-simulate'),
    path('webhook/',  PaymentWebhookView.as_view(),  name='payment-webhook'),
]