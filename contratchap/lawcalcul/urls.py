# urls.py
from django.urls import path
from .views import SimulationCalculView, SimulationAdminListView

urlpatterns = [
    # ... tes autres routes ...
    
    # URL pour lancer la simulation des droits
    path('simulations/calculer/', SimulationCalculView.as_view(), name='calculer-droits-rupture'),
    # ⚡️ NOUVELLE URL : Pour récupérer l'historique dans le dashboard admin
    path('simulations/', SimulationAdminListView.as_view(), name='liste-simulations-admin'),
]