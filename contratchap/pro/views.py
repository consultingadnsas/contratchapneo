from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Country, LegalDomain, LegalProfessional
from .serializers import CountrySerializer, LegalDomainSerializer, LegalProfessionalSerializer

class LegalProfessionalListView(APIView):
    """
    Récupère la liste des professionnels du droit avec filtres.
    URL attendue : /api/professionals/?country=CI&domain=droit-des-societes&q=Dakar
    """
    # L'annuaire est public, pas besoin d'être connecté
    permission_classes = [] 
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # 1. Base de la requête optimisée (Adieu les requêtes N+1 !)
        professionals = LegalProfessional.objects.filter(is_active=True)\
            .select_related('country')\
            .prefetch_related('domains')
        
        # 2. Récupération des paramètres de l'URL (?country=...&domain=...&q=...)
        country_code = request.query_params.get('country')
        domain_slug = request.query_params.get('domain')
        search_query = request.query_params.get('q')

        # 3. Application des filtres conditionnels
        if country_code:
            professionals = professionals.filter(country__code__iexact=country_code)
        
        if domain_slug:
            professionals = professionals.filter(domains__slug__iexact=domain_slug)
        
        if search_query:
            # Recherche textuelle dans le nom, prénom ou la ville
            professionals = professionals.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query) |
                Q(city__icontains=search_query)
            )

        # 4. Sérialisation et Réponse (context={'request': request} permet de construire les URLs absolues des photos)
        serializer = LegalProfessionalSerializer(professionals, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Bonus : Les vues pour alimenter les menus déroulants de Nuxt ---

class FilterOptionsView(APIView):
    """
    Une seule APIView pour renvoyer les pays et domaines disponibles 
    pour tes menus déroulants de filtrage sur le Frontend.
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # On ne renvoie que les pays/domaines qui ont au moins un professionnel actif
        countries = Country.objects.filter(professionals__is_active=True).distinct()
        domains = LegalDomain.objects.filter(professionals__is_active=True).distinct()

        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'domains': LegalDomainSerializer(domains, many=True).data
        }, status=status.HTTP_200_OK)