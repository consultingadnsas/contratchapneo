# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny # Mets IsAuthenticated si l'utilisateur doit être connecté

from .serializers import SimulationDroitsSerializer
from .utils import calculer_droits

class SimulationCalculView(APIView):
    """
    POST /api/simulations/calculer/
    Reçoit les données RH, les valide, les sauvegarde et retourne le calcul des droits.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. On passe les données au sérialiseur
        serializer = SimulationDroitsSerializer(data=request.data)
        
        # L'astuce magique de DRF : si les données sont invalides, ça renvoie une erreur 400 direct !
        serializer.is_valid(raise_exception=True)
        
        # 2. On sauvegarde en base de données pour l'historique
        simulation_instance = serializer.save()
        
        # 3. On appelle notre cerveau mathématique
        resultats_calcul = calculer_droits(simulation_instance)
        
        # 4. On renvoie la réponse formatée pour ton interface Nuxt/Vue
        return Response(
            {
                "message": "Simulation effectuée avec succès.",
                "donnees_saisies": serializer.data,
                "resultats_financiers": resultats_calcul
            },
            status=status.HTTP_201_CREATED
        )