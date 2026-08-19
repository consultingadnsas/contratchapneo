from rest_framework import serializers
from .models import Category, Contrat, CustomedContract, Pack, UserPack, ContractRevision
from account.models import CustomUser
from ecommerce.models import GuestInfo

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
            'promo_price',
            'fichier_modele',
            'picture', 
            'views', 
            'downloads',
            'is_active',
            'created_at', 
            'updated_at'
        ]

class CustomedContractSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomedContract
        fields = [
            'id', 'subject', 'phone_number', 'email', 'description', 
            'price', 'is_wrotten', 'user', 'user_pack', 
            'client_name', 'category','created_at', 'category_name', 'updated_at'
        ]
        read_only_fields = ['id', 'is_wrotten', 'user', 'user_pack', 'client_name', 'category_name', 'created_at', 'updated_at']

    def get_client_name(self, obj):
        # 1. Si l'utilisateur est connecté (CustomUser)
        if obj.user:
            first_name = getattr(obj.user, 'first_name', '')
            last_name = getattr(obj.user, 'last_name', '')
            full_name = f"{first_name} {last_name}".strip()
            if full_name:
                return full_name

        # 2. S'il n'est pas connecté, on cherche dans GuestInfo via l'email
        if obj.email:
            # On prend la toute dernière info associée à cet email
            guest = GuestInfo.objects.filter(email=obj.email).order_by('-created_at').first()
            if guest and guest.full_name:
                return guest.full_name.strip()

        return None
    
    def get_category_name(self, obj):
        if obj.category:
            return obj.category.title
        return "Catégorie non spécifiée"

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

# Dans contrat/serializers.py
class PackModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack  # le modèle original
        fields = [
            'id', 
            'title', 
            'description', 
            'prix',
            'prix_promo', # ⚡️ Ajouté
            'nombre_credits', # ⚡️ Ajouté
            'custom_contract_included', # ⚡️ Ajouté
            'nombre_customed_contract', # ⚡️ Ajouté
            'consultation_pro_incluse', # ⚡️ Ajouté
            'nombre_cartes_pro', # ⚡️ Ajouté
            'duree_validite_jours', # ⚡️ Ajouté
            'picture', 
            'created_at'
        ]

class AdminPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = '__all__' # Expose tous les champs du modèle

class ContractRevisionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    client_name = serializers.SerializerMethodField(read_only=True)
    original_file = serializers.FileField(required=True)

    class Meta:
        model = ContractRevision
        fields = [
            'id', 'subject', 'phone_number', 'email', 'client_instructions',
            'original_file', 'revised_file', 'price', 'promo_price', 'status',
            'status_display', 'is_revised', 'expert_comments', 'user', 'user_pack',
            'client_name', # ⚡️ Le champ calculé
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'revised_file', 'price', 'promo_price', 'status', 
            'status_display', 'is_revised', 'expert_comments', 'user', 
            'user_pack', 'client_name', 'created_at', 'updated_at'
        ]

    def get_client_name(self, obj):
        # 1. CustomUser
        if obj.user:
            first_name = getattr(obj.user, 'first_name', '')
            last_name = getattr(obj.user, 'last_name', '')
            full_name = f"{first_name} {last_name}".strip()
            if full_name:
                return full_name

        # 2. GuestInfo
        if obj.email:
            guest = GuestInfo.objects.filter(email=obj.email).order_by('-created_at').first()
            if guest and guest.full_name:
                return guest.full_name.strip()

        return None