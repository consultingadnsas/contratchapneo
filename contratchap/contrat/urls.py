from django.urls import path
from .views import (
    CategoryDetailWithContractsView, 
    CategoryListView, 
    CategoryOperationsView,
    ContractListView,
    ContractsView,
    ContratOperationsView,
    ContractTagsView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/operations/', CategoryOperationsView.as_view(), name='category-operations'),
    path('categories/<uuid:category_id>/', CategoryDetailWithContractsView.as_view(), name='category-detail-with-contracts'),
    
    # Specific contract
    path('', ContractListView.as_view(), name='contract-list'),
    path('operations/', ContratOperationsView.as_view(), name='contrat-operations'),
    path('<uuid:contrat_id>/',ContractsView.as_view(), name="contrats"),

    # Contract tag
    path('tags/<uuid:contrat_id>/', ContractTagsView.as_view(), name='contract-tags')
]