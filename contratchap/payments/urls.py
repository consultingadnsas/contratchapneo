# urls.py
from django.urls import path
from .views import PaymentInitiateView, PaymentSimulateView, PaymentWebhookView, DownloadContractView

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('simulate/', PaymentSimulateView.as_view(), name='payment-simulate'),
    path('webhook/',  PaymentWebhookView.as_view(),  name='payment-webhook'),
    # 👇 Nouvelle route pour le téléchargement
    path('download/<str:order_id>/', DownloadContractView.as_view(), name='download-contract'),
]