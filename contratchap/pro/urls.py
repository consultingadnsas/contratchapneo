from django.urls import path
# pyrefly: ignore [missing-import]
from .views import (
    CountryAdminView,
    DomainAdminView,
    LegalProfessionalListView, 
    FilterOptionsView,
    DownloadProCardFromPack,
    ProAdminView,
    LegalProfessionalRegistrationView
)

urlpatterns = [
    path('registration/', LegalProfessionalRegistrationView.as_view(), name='pro-registration'),
    path('professionals/', LegalProfessionalListView.as_view(), name='professional-list'),
    path('professionals/filters/', FilterOptionsView.as_view(), name='professional-filters'),
    path('professionals/download/<uuid:pro_id>/', DownloadProCardFromPack.as_view(), name='download-pro-card'),
    path('admin/', ProAdminView.as_view(), name="pro-admin"),
    path('admin/<uuid:pro_id>/', ProAdminView.as_view()),
    path('countries/admin/', CountryAdminView.as_view(), name='country-admin'),
    path('countries/admin/<int:country_id>/', CountryAdminView.as_view(), name='country-admin-detail'),
    path('domains/admin/', DomainAdminView.as_view(), name='domain-admin'),
    path('domains/admin/<int:domain_id>/', DomainAdminView.as_view(), name='domain-admin-detail'),
]