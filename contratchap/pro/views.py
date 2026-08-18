import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Country, LegalDomain, LegalProfessional, ProCardDownload
from .serializers import CountrySerializer, LegalDomainSerializer, LegalProfessionalSerializer, LegalProfessionalRegistrationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from contrat.models import UserPack
from django.http import FileResponse
from django.utils.text import slugify
from django.db import transaction

class LegalProfessionalRegistrationView(APIView):
    """
    POST /register/professional/
    Accepts nested user data + professional fields.
    Returns the created professional data (with nested country/domains).
    """
    permission_classes = []   # Public access

    def post(self, request, format=None):
        serializer = LegalProfessionalRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            professional = serializer.save()

            # Use a read‑only serializer to return full nested objects (country, domains, etc.)
            output_serializer = LegalProfessionalSerializer(professional)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
class DownloadProCardFromPack(APIView):
    """
    POST /pros/<pro_id>/download-card/
    Télécharge la carte de visite d'un professionnel en utilisant
    un crédit du pack actif de l'utilisateur.

    Règles :
        - Si le user a déjà téléchargé la carte de ce pro, pas de nouveau crédit débité.
        - Le crédit n'est déduit que si le fichier est confirmé lisible.
        - La déduction + création du log sont atomiques (select_for_update).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pro_id):
        user = request.user
        pro = get_object_or_404(LegalProfessional, id=pro_id)

        if not pro.visiting_card or not hasattr(pro.visiting_card, 'path'):
            return Response(
                {"error": "Ce professionnel n'a pas de carte de visite disponible."},
                status=status.HTTP_404_NOT_FOUND
            )

        file_path = pro.visiting_card.path
        if not os.path.exists(file_path):
            return Response(
                {"error": "Le fichier est introuvable sur le serveur."},
                status=status.HTTP_404_NOT_FOUND
            )

        # On cherche un pack valide qui a DÉJÀ débloqué ce pro (téléchargement gratuit)
        user_pack_avec_acces = (
            UserPack.objects
            .filter(user=user, is_active=True, pros_debloques=pro)
            .first()
        )

        if not user_pack_avec_acces:
            # Sinon on cherche un pack avec du crédit dispo pour en débloquer un nouveau
            try:
                with transaction.atomic():
                    user_pack = (
                        UserPack.objects
                        .select_for_update()
                        .filter(user=user, is_active=True, cartes_pro_restantes__gt=0)
                        .order_by('purchased_at')  # on consomme les plus anciens packs en premier
                        .first()
                    )

                    if not user_pack or not user_pack.is_valid:
                        return Response(
                            {"error": "Vous n'avez plus de cartes de pro disponibles dans vos packs."},
                            status=status.HTTP_403_FORBIDDEN
                        )

                    user_pack.cartes_pro_restantes -= 1
                    user_pack.save()
                    user_pack.pros_debloques.add(pro)

            except Exception as e:
                return Response(
                    {"error": "Erreur lors de la déduction du crédit.", "detail": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Envoi du fichier (identique à avant)
        nom_fichier = (
            slugify(f"Carte_visite_{pro.first_name}_{pro.last_name}") + ".pdf"
            if pro.first_name else "carte-visite-pro.pdf"
        )
        try:
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
        except (FileNotFoundError, OSError):
            return Response(
                {"error": "Le fichier est introuvable sur le serveur."},
                status=status.HTTP_404_NOT_FOUND
            )

# ==============================================================================
# 1. Gestion des pro côté
# ==============================================================================

class ProAdminView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        # On ne met pas le try/except global sur la validation
        serializer = LegalProfessionalSerializer(data=request.data, context={'request': request})
        
        # Au lieu de raise_exception=True qui fait crasher si mal géré, 
        # on vérifie proprement et on renvoie les erreurs détaillées.
        if not serializer.is_valid():
            # Renverra par exemple {"email": ["Un utilisateur avec cet email existe déjà."]} en statut 400
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response(
                {"data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Erreur critique lors de la sauvegarde : {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        pro = LegalProfessional.objects.all()
        # ⚡️ LA CORRECTION EST ICI : on ajoute context={'request': request}
        serializer = LegalProfessionalSerializer(pro, many=True, context={'request': request})

        return Response(
            {
                "data": serializer.data
            }, status=status.HTTP_200_OK
        )

    def put(self, request, pro_id):
        """ Mise à jour des packs """
        pro = get_object_or_404(LegalProfessional, id=pro_id)
        # ⚡️ Ajout du contexte
        serializer = LegalProfessionalSerializer(pro, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Pro mis à jour'
                },
                status=status.HTTP_200_OK
            )
        # (Optionnel : pense à rajouter un return d'erreur si le serializer n'est pas valide)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # (La méthode delete reste inchangée)