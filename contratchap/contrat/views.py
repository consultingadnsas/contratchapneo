from docxtpl import DocxTemplate
from django.http import FileResponse
import tempfile
import os
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from .models import Category, Contrat, CustomedContract, Pack, UserPack
from .serializers import (
    CategorySerializer, 
    ContratSerializer, 
    CategoryWithContractsSerializer,
    CustomedContractSerializer,
    PackModelSerializer
)

from docx import Document
from .utils import extract_tags_grouped_by_paragraph, convert_docx_to_pdf

class ContratPagination(PageNumberPagination):
    page_size = 10  # 10 éléments par page
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.

class CategoryListView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        categories = Category.objects.all()
        data = [
            {
                'id': str(category.id),
                'title': category.title,
                'description': category.description,
                'created_at': category.created_at,
                'updated_at': category.updated_at
            }
            for category in categories
        ]
        return Response(data, status=status.HTTP_200_OK)
    
class CategoryDetailWithContractsView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, category_id):
        # On récupère la catégorie ou on renvoie une erreur 404 si elle n'existe pas
        # prefetch_related permet de charger efficacement tous les contrats liés
        category = get_object_or_404(
            Category.objects.prefetch_related('contrats'), 
            id=category_id
        )
        
        # On passe l'instance au serializer
        serializer = CategoryWithContractsSerializer(category, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryOperationsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serializer = CategorySerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        'data': serializer.data,
                        'message': 'Catégorie créée avec succès'
                    }, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'errors': serializer.errors,
                    'message': 'Erreur lors de la création de la catégorie'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Erreur lors de la création de la catégorie',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
""" About our contrat """

class ContractListView(ListAPIView):
    """
    Vue pour lister tous les contrats, avec possibilité de filtrer par catégorie
    via le paramètre de requête ?category=<uuid>
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    # DRF s'occupe de lier le bon serializer et la pagination automatiquement
    serializer_class = ContratSerializer
    pagination_class = ContratPagination

    def get_queryset(self):
        # Toujours penser au order_by !
        queryset = Contrat.objects.select_related('category').order_by('-created_at')
        
        # self.request est automatiquement disponible dans les vues génériques
        category_id = self.request.query_params.get('category', None)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search_query = self.request.query_params.get('q', None)
        if search_query:
            # Recherche insensible à la casse (icontains) sur le titre OU la description
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        return queryset


class ContractsView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, contrat_id):
        # 1. Récupération du contrat
        contrat = get_object_or_404(
            Contrat.objects.all(),
            id=contrat_id
        )

        # 2. Incrémentation du compteur de vues
        contrat.views = F('views') + 1
        contrat.save(update_fields=['views'])

        # 3. Sérialisation des données de base (JSON)
        serializer = ContratSerializer(contrat, context={'request': request})
        data = serializer.data  # On extrait le dictionnaire des données

        # 4. Extraction de l'aperçu du DOCX (Simulation de la première page)
        try:
            if contrat.fichier_modele and hasattr(contrat.fichier_modele, 'path'):
                # Ouverture du document Word
                doc = Document(contrat.fichier_modele.path)
                
                # On va stocker les premiers paragraphes pour faire l'aperçu
                preview_paragraphs = []
                
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if text: # On ignore les lignes vides
                        preview_paragraphs.append(text)
                    
                    # On s'arrête à 15 paragraphes (tu peux ajuster ce chiffre pour simuler une "page" A4)
                    if len(preview_paragraphs) >= 10:
                        break
                
                # On joint les paragraphes avec un double saut de ligne
                data['document_preview'] = "\n\n".join(preview_paragraphs)
            else:
                data['document_preview'] = None
        except Exception as e:
            # En cas de pépin avec le fichier, on ne bloque pas l'API
            data['document_preview'] = None
            data['document_preview_error'] = str(e)

        # 5. Envoi de la réponse combinée
        return Response(data, status=status.HTTP_200_OK)
    
class ContratOperationsView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ContratSerializer(data = request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        'data': serializer.data,
                        'message': 'Contrat créée avec succès'
                    }, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'errors': serializer.errors,
                    'message': 'Erreur lors de la création du contrat'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Erreur lors de l\'ajout du contrat',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CustomedContractRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CustomedContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Demande de contrat sur mesure enregistrée avec succès.'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'errors': serializer.errors,
                'message': 'Impossible de créer la demande sur mesure.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ContractTagsView(APIView):

    permission_classes = [AllowAny]
    permission_classes = []

    def get(self, request, contrat_id):

        # Récupère le contrat
        contrat = Contrat.objects.get(id=contrat_id)

        # Le chemin physique du fichier docx
        file_path = contrat.fichier_modele.path

        # Extraire les balises
        tags = extract_tags_grouped_by_paragraph(file_path=file_path)

        return Response({"tags": tags})
    
    def post(self, request, contrat_id):
        
        try:
            # 1. Récupération du contrat
            contrat = get_object_or_404(Contrat, id=contrat_id)
            
            # 2. Récupération des données du formulaire (envoyées par le frontend)
            user_inputs = request.data.get('user_inputs', {})

            # 3. Remplissage du template Word
            doc = DocxTemplate(contrat.fichier_modele.path)
            doc.render(user_inputs)

            # 4. Création d'un dossier temporaire unique
            # On utilise un contexte pour s'assurer que le fichier est bien créé
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
                doc.save(tmp_docx.name)
                tmp_docx_path = tmp_docx.name

            # 5. Conversion en PDF via ta fonction utils
            pdf_path = convert_docx_to_pdf(tmp_docx_path)

            # 6. Envoi du fichier en réponse
            pdf_file = open(pdf_path, 'rb')
            response = FileResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="contrat_{contrat.title}.pdf"'

            # 🧹 Nettoyage optionnel (pour éviter de saturer le serveur)
            # Tu pourrais ajouter un petit thread ici ou un simple cleanup différé
            # os.remove(tmp_docx_path)
            # os.remove(pdf_path)

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)

# ==========================================
# 1 Manage all about packs
# ==========================================

class PacksView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):

        """ Vue pour récupérer tous les packs que nous proposons"""

        pack = Pack.objects.all()

        serializer = PackModelSerializer(pack, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# ==========================================
# 1- Download contract once authenticated
# ==========================================

class DownloadContractFromPack(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, contract_id):
        # 1. Récupération du contrat
        contrat = get_object_or_404(Contrat, id=contract_id)
        user = request.user

        # 2. Vérification du pack de l'utilisateur
        user_pack = UserPack.objects.filter(user=user, is_active=True).first()

        if not user_pack:
            return Response(
                {"error": "Vous n'avez aucun pack actif pour télécharger ce contrat."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Vérification préalable du modèle (avant de toucher aux crédits)
        if not contrat.fichier_modele or not contrat.fichier_modele.path:
            return Response(
                {"error": "Ce contrat ne possède pas de modèle disponible pour la génération."},
                status=status.HTTP_404_NOT_FOUND
            )

        already_unlocked = contrat in user_pack.contrats_choisis.all()

        # On vérifie les crédits AVANT de générer, pour échouer vite si besoin
        if not already_unlocked and user_pack.credits_restants <= 0:
            return Response(
                {"error": "Vous n'avez plus de crédits disponibles dans votre pack."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 4. Génération dynamique du fichier — AVANT tout débit de crédit
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                user_inputs = request.data.get('user_inputs', {})

                # Remplissage du template Word
                doc = DocxTemplate(contrat.fichier_modele.path)
                doc.render(user_inputs)

                tmp_docx_path = os.path.join(temp_dir, f"temp_{contrat.id}.docx")
                doc.save(tmp_docx_path)

                # Conversion en PDF — même signature que OrderDownloadView
                convert_docx_to_pdf(tmp_docx_path, temp_dir)
                generated_temp_pdf = os.path.join(temp_dir, f"temp_{contrat.id}.pdf")

                if not os.path.exists(generated_temp_pdf):
                    return Response(
                        {"error": "Erreur lors de la conversion du document en PDF."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                # On lit les bytes du PDF AVANT que le TemporaryDirectory ne soit nettoyé
                with open(generated_temp_pdf, 'rb') as f:
                    pdf_bytes = f.read()

            except Exception as e:
                return Response(
                    {"error": f"Erreur lors de la génération du document : {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # 5. La génération a réussi : on débloque et on décrémente le crédit, de façon atomique
        if not already_unlocked:
            with transaction.atomic():
                # On reverrouille la ligne pour éviter une race condition sur credits_restants
                locked_pack = UserPack.objects.select_for_update().get(pk=user_pack.pk)

                if locked_pack.credits_restants <= 0:
                    return Response(
                        {"error": "Vous n'avez plus de crédits disponibles dans votre pack."},
                        status=status.HTTP_403_FORBIDDEN
                    )

                locked_pack.contrats_choisis.add(contrat)
                locked_pack.credits_restants = F('credits_restants') - 1
                locked_pack.save(update_fields=['credits_restants'])

        # 6. Envoi du fichier en réponse (depuis les bytes déjà lus en mémoire)
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)

        safe_title = "".join(c for c in contrat.title if c.isalnum() or c in " _-").rstrip()
        response = FileResponse(
            buffer,
            as_attachment=True,
            filename=f"contrat_{safe_title}.pdf",
            content_type='application/pdf'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response

# ==========================================
# 2. URL: /contract/packs/custom_contract/
# ==========================================

class CustomContractFromPack(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Crée une demande de contrat sur mesure en utilisant un crédit
        'customs_restants' d'un pack actif de l'utilisateur.
        """
        user = request.user

        # 1. Récupération du pack actif de l'utilisateur qui inclut le sur-mesure
        user_pack = UserPack.objects.filter(
            user=user,
            is_active=True,
            pack__custom_contract_included=True
        ).select_related('pack').order_by('-purchased_at').first()

        if not user_pack:
            return Response(
                {"error": "Vous n'avez aucun pack actif incluant les contrats sur mesure."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Vérification de la validité (expiration incluse)
        if not user_pack.is_valid:
            return Response(
                {"error": "Votre pack a expiré ou n'est plus actif."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Vérification des crédits sur mesure restants
        if user_pack.customs_restants <= 0:
            return Response(
                {"error": "Vous n'avez plus de crédits disponibles pour un contrat sur mesure."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 4. Validation des données de la demande
        serializer = CustomedContractSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'errors': serializer.errors,
                    'message': 'Impossible de créer la demande sur mesure.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Création + débit du crédit, de façon atomique
        try:
            with transaction.atomic():
                # On reverrouille la ligne pour éviter une race condition
                locked_pack = UserPack.objects.select_for_update().get(pk=user_pack.pk)

                if locked_pack.customs_restants <= 0:
                    return Response(
                        {"error": "Vous n'avez plus de crédits disponibles pour un contrat sur mesure."},
                        status=status.HTTP_403_FORBIDDEN
                    )

                custom_contract = serializer.save(
                    user=user,
                    user_pack=locked_pack,
                )

                locked_pack.customs_restants = F('customs_restants') - 1
                locked_pack.save(update_fields=['customs_restants'])

        except Exception as e:
            return Response(
                {
                    'message': 'Erreur lors de la création de la demande sur mesure.',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'data': CustomedContractSerializer(custom_contract).data,
                'message': 'Votre demande de contrat sur mesure a été envoyée avec succès. '
                           f'Il vous reste {locked_pack.customs_restants} crédit(s) sur mesure.'
            },
            status=status.HTTP_201_CREATED
        )

# ==========================================
# 1. URL: /api/admin/contracts/
# ==========================================
class AdminContractListCreateView(APIView):
    
    permission_classes = [IsAdminUser]

    def post(self, request):
        
        """ 
            Création d'un nouveau contrat 
        """
        # On passe le contexte pour la gestion des URLs des fichiers si nécessaire
        serializer = ContratSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Contrat créé avec succès'
                }, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': serializer.errors,
                'message': 'Erreur lors de la création du contrat'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


# ==============================================
# 2. URL: /api/admin/contracts/<int:contrat_id>/
# ==============================================
class AdminContractDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, contrat_id):
        """Récupération d'un contrat spécifique avec sa catégorie"""
        contract = get_object_or_404(
            Contrat.objects.select_related('category'), 
            id=contrat_id
        )
        serializer = ContratSerializer(contract, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, contrat_id):
        """Mise à jour d'un contrat spécifique"""
        contract = get_object_or_404(Contrat, id=contrat_id)

        # Note: partial=True permet une mise à jour partielle (comportement d'un PATCH)
        serializer = ContratSerializer(contract, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Contrat mis à jour avec succès'
                }, 
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                'error': serializer.errors,
                'message': 'Erreur lors de la mise à jour du contrat'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, contrat_id):
        """Suppression d'un contrat spécifique"""
        contract = get_object_or_404(Contrat, id=contrat_id)
        contract.delete()
        # En REST, une suppression réussie retourne généralement un statut 204 No Content
        return Response(
            {"message": "Contrat supprimé avec succès"}, 
            status=status.HTTP_204_NO_CONTENT
        )

# ==========================================
# 3. URL: /api/admin/contract/
# ==========================================

class AdminCategoryDetail(APIView):

    permission_classes=[IsAdminUser]

    def post(self, request):

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Catégorie ajoutée avec succès'
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': serializer.errors,
                'message': 'Erreur lors de la création de la catégorie'
            },
            status=status.HTTP_400_BAD_REQUEST
        )