from django.urls import path
from .views import AdminDailyVisitView, VisitAPIView

urlpatterns = [
    # ... tes autres routes ...
    path('admin/visitors/', AdminDailyVisitView.as_view(), name='admin-visitors'),
    path('visit/', VisitAPIView.as_view(), name='public-visit'),
]