import io
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from pypdf import PdfReader, PdfWriter
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from .models import Category, Contrat
from .serializers import (
    CategorySerializer, 
    ContratSerializer, 
    CategoryWithContractsSerializer
)
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
        serializer = CategoryWithContractsSerializer(category)
        
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

class ContractListView(APIView):
    """
    Vue pour lister tous les contrats, avec possibilité de filtrer par catégorie
    via le paramètre de requête ?category=<uuid>
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        # On récupère le paramètre 'category' depuis l'URL (ex: /contrat/?category=UUID)
        category_id = request.query_params.get('category', None)

        # Base de la requête : on sélectionne tous les contrats
        # select_related('category') permet d'optimiser la requête SQL en joignant la table catégorie
        queryset = Contrat.objects.all().select_related('category')

        # Si le paramètre category est fourni, on filtre les résultats
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Sérialisation de la liste des contrats
        serializer = ContratSerializer(queryset, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        serializer = ContratSerializer(contrat)
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