from django.urls import path
from .views import AdminDailyVisitView

urlpatterns = [
    # ... tes autres routes ...
    path('admin/visitors/', AdminDailyVisitView.as_view(), name='admin-visitors'),
]