# urls.py
from django.urls import path
from .views import SimulationCalculView

urlpatterns = [
    # ... tes autres routes ...
    
    # URL pour lancer la simulation des droits
    path('simulations/calculer/', SimulationCalculView.as_view(), name='calculer-droits-rupture'),
]