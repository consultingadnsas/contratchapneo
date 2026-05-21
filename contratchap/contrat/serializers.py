from rest_framework import serializers
from .models import Category, Contrat

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id', 
            'title', 
            'description', 
            'created_at', 
            'updated_at'
        ]

class ContratSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contrat
        fields = [
            'id', 
            'category', 
            'title', 
            'description', 
            'prix', 
            'fichier_modele',
            'picture', 
            'views', 
            'downloads', 
            'created_at', 
            'updated_at'
        ]

class CategoryWithContractsSerializer(serializers.ModelSerializer):
    # On utilise le related_name défini dans le modèle Contrat
    # many=True indique qu'une catégorie peut avoir plusieurs contrats
    contrats = ContratSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 
            'title', 
            'description', 
            'contrats',  # On ajoute le champ ici
            'created_at', 
            'updated_at'
        ]