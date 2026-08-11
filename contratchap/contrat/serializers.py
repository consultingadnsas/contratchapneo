from rest_framework import serializers
from .models import Category, Contrat, CustomedContract, Pack, UserPack, ContractRevision
from account.models import CustomUser

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
            'user',
            'user_pack',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_wrotten', 'user', 'user_pack', 'created_at', 'updated_at']

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

# Dans contrat/serializers.py
class PackModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack  # le modèle original
        fields = [
            'id', 
            'title', 
            'description', 
            'prix', 
            'picture', 
            'created_at'
        ]  # adaptez

class AdminPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = '__all__' # Expose tous les champs du modèle

class ContractRevisionSerializer(serializers.ModelSerializer):
    # 💡 Petit bonus Contratchap : On ajoute ce champ pour que ton front-end 
    # récupère directement "En attente" au lieu de "PENDING"
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    original_file = serializers.FileField(required=True)

    class Meta:
        model = ContractRevision
        fields = [
            'id',
            'subject',
            'phone_number',
            'email',
            'client_instructions',
            'original_file',  # Le fichier soumis par le client
            'revised_file',   # Le fichier renvoyé par le juriste
            'price',
            'promo_price',
            'status',
            'status_display',
            'is_revised',
            'expert_comments',
            'user',
            'user_pack',
            'created_at',
            'updated_at',
        ]
        
        # 🚨 TRÈS IMPORTANT : On verrouille tous les champs que l'utilisateur 
        # ne doit pas pouvoir manipuler lors de la soumission de sa demande.
        read_only_fields = [
            'id', 
            'revised_file', 
            'price', 
            'promo_price', 
            'status', 
            'status_display', 
            'is_revised', 
            'expert_comments', 
            'user', 
            'user_pack', 
            'created_at', 
            'updated_at'
        ]

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

    def validate_client_instructions(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('Les instructions doivent être un peu plus détaillées pour guider nos juristes.')
        return value.strip()

    def validate_email(self, value):
        return value.lower().strip()