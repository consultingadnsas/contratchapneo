from rest_framework import serializers
from .models import Country, LegalDomain, LegalProfessional
from account.serializers import UserSerializer

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'is_ohada_member']

class LegalDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDomain
        fields = ['id', 'name', 'slug']

class LegalProfessionalSerializer(serializers.ModelSerializer):
    # On imbrique les sérialiseurs pour que Nuxt reçoive l'objet Pays et Domaines complets, pas juste leurs IDs
    country = CountrySerializer(read_only=True)
    domains = LegalDomainSerializer(many=True, read_only=True)
    
    # Pour envoyer la version lisible du titre (ex: "Avocat" au lieu de "AVOCAT")
    title_display = serializers.CharField(source='get_title_display', read_only=True)

    class Meta:
        model = LegalProfessional
        # On exclut le user Django pour des raisons de sécurité
        exclude = ['user']

class LegalProfessionalRegistrationSerializer(serializers.ModelSerializer):
    # Nested user serializer – make it writable
    user = UserSerializer()

    # Accept country and domains by ID for creation (or by nested objects if you prefer)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    domains = serializers.PrimaryKeyRelatedField(many=True, queryset=LegalDomain.objects.all())

    class Meta:
        model = LegalProfessional
        fields = [
            'user',          # nested user data
            'title',
            'professional_order',
            'registration_number',
            'email',         # if you keep email on professional (optional)
            'phone_number',
            'website',
            'profile_picture',
            'visiting_card',
            'bio',
            'years_of_experience',
            'prix',
            'country',
            'city',
            'domains',
        ]
        # Do not include 'is_active', 'is_verified', 'created_at', etc. – they are set automatically

    def create(self, validated_data):
        # Extract user data
        user_data = validated_data.pop('user')
        # Extract many-to-many domains (they are not saved yet)
        domains = validated_data.pop('domains')

        # Create the CustomUser (handles password hashing if UserSerializer does it)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Create the LegalProfessional profile, linking to the new user
        professional = LegalProfessional.objects.create(user=user, **validated_data)

        # Set many-to-many relations
        professional.domains.set(domains)

        return professional