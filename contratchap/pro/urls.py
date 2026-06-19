from django.urls import path
from .views import LegalProfessionalListView, FilterOptionsView

urlpatterns = [
    path('professionals/', LegalProfessionalListView.as_view(), name='professional-list'),
    path('professionals/filters/', FilterOptionsView.as_view(), name='professional-filters'),
]