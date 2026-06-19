from rest_framework import serializers
from .models import Country, LegalDomain, LegalProfessional

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