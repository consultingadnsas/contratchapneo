import io
import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from .models import Category, Contrat
from .serializers import (
    CategorySerializer, 
    ContratSerializer, 
    CategoryWithContractsSerializer
)

from pypdf import PdfReader, PdfWriter
from .utils import extract_tags_from_docx

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

from rest_framework.generics import ListAPIView

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

        # 4. Extraction sécurisée de la première page du PDF
        try:
            if contrat.fichier_modele and hasattr(contrat.fichier_modele, 'path'):
                reader = PdfReader(contrat.fichier_modele.path)
                
                if len(reader.pages) > 0:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[0])  # Uniquement la page 1
                    
                    # Écriture dans un flux mémoire
                    buffer = io.BytesIO()
                    writer.write(buffer)
                    buffer.seek(0)
                    
                    # Transformation en chaîne Base64
                    encoded_pdf = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # On ajoute le PDF au format Data URI dans le JSON
                    data['pdf_preview'] = f"data:application/pdf;base64,{encoded_pdf}"
                else:
                    data['pdf_preview'] = None
            else:
                data['pdf_preview'] = None
        except Exception as e:
            # En cas de pépin avec le fichier, on ne bloque pas l'API, on met juste la preview à None
            data['pdf_preview'] = None
            data['pdf_preview_error'] = str(e)

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
        
class ContractTagsView(APIView):

    permission_classes = [AllowAny]
    permission_classes = []

    def get(self, request, contrat_id):

        # Récupère le contrat
        contrat = Contrat.objects.get(id=contrat_id)

        # Le chemin physique du fichier docx
        file_path = contrat.fichier_modele.path

        # Extraire les balises
        tags = extract_tags_from_docx(file_path=file_path)

        return Response({"tags": tags})