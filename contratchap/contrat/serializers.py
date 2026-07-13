from rest_framework import serializers
from .models import Category, Contrat, CustomedContract, Pack, UserPack

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

class CustomedContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomedContract
        fields = [
            'id',
            'subject',
            'phone_number',
            'email',
            'description',
            'price',
            'is_wrotten',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'is_wrotten', 'created_at', 'updated_at']

    def validate_subject(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('Le sujet est trop court.')
        return value.strip()

    def validate_phone_number(self, value):
        import re
        cleaned = re.sub(r'\s+', '', value.strip())
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError('Numéro de téléphone invalide. Ex : +2250701234567 ou 0701234567.')
        return cleaned

    def validate_description(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError('La description doit être plus détaillée.')
        return value.strip()

    def validate_email(self, value):
        return value.lower().strip()

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

class PackSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserPack
        fields = '__all__'