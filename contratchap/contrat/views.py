from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import Category, Contrat
from .serializers import (
    CategorySerializer, 
    ContratSerializer, 
    CategoryWithContractsSerializer
)
# Create your views here.

class CategoryListView(APIView):

    permission_classes = [AllowAny]

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