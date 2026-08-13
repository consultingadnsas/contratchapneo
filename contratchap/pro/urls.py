from django.urls import path
from .views import (
    LegalProfessionalListView, 
    FilterOptionsView,
    DownloadProCardFromPack,
    ProAdminView
)

urlpatterns = [
    path('professionals/', LegalProfessionalListView.as_view(), name='professional-list'),
    path('professionals/filters/', FilterOptionsView.as_view(), name='professional-filters'),
    path('professionals/download/<uuid:pro_id>/', DownloadProCardFromPack.as_view(), name='download-pro-card'),
    path('admin/', ProAdminView.as_view(), name="pro-admin"),
    path('admin/<uuid:pro_id>/', ProAdminView.as_view()),
]