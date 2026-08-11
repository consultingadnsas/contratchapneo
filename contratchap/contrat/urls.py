from django.urls import path
from .views import (
    CategoryDetailWithContractsView, 
    CategoryListView, 
    CategoryOperationsView,
    ContractListView,
    ContractsView,
    ContratOperationsView,
    CustomedContractRequestView,
    ContractRevisionRequestView,
    ContractTagsView,
    PacksView,
    DownloadContractFromPack,
    CustomContractFromPack,
    AdminCategory,
    AdminContractListCreateView,
    AdminPackView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/operations/', CategoryOperationsView.as_view(), name='category-operations'),
    path('categories/<uuid:category_id>/', CategoryDetailWithContractsView.as_view(), name='category-detail-with-contracts'),
    
    # Specific contract
    path('', ContractListView.as_view(), name='contract-list'),
    path('operations/', ContratOperationsView.as_view(), name='contrat-operations'),
    path('<uuid:contrat_id>/',ContractsView.as_view(), name="contrats"),

    # Packs
    path('packs/', PacksView.as_view(), name="pack-view"),
    path('packs/downloads/<uuid:contract_id>/', DownloadContractFromPack.as_view(), name="packs-download"),
    path('packs/custom_contract/', CustomContractFromPack.as_view(), name='custom_contract'),

    # Contract tag
    path('tags/<uuid:contrat_id>/', ContractTagsView.as_view(), name='contract-tags'),

    # Admin endpoints:
    path('admin-category/', AdminCategory.as_view(), name='admin-category'),
    path('custom-requests/', CustomedContractRequestView.as_view(), name='custom-contract-requests'),
    path('revision-requests/', ContractRevisionRequestView.as_view(), name='contract-revision-requests'),
    path('admin-contrat/', AdminContractListCreateView.as_view(), name="admin-contract"),
    path('admin-pack/', AdminPackView.as_view(), name="admin-views")
]