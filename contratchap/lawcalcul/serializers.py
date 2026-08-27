from rest_framework import serializers
from .models import SimulationDroits
from .utils import calculer_droits

class SimulationDroitsSerializer(serializers.ModelSerializer):
    resultats_financiers = serializers.SerializerMethodField()

    class Meta:
        model = SimulationDroits
        fields = '__all__'

    def get_resultats_financiers(self, obj):
        # On repasse l'instance à ton "cerveau mathématique"
        try:
            return calculer_droits(obj)
        except Exception:
            return None # En cas d'erreur de calcul sur une vieille donnée

    def validate_email(self, value):
            return value.lower().strip()

    def validate_salaires_12_mois(self, value):
        """ Vérifie que c'est bien une liste d'exactement 12 éléments (ou moins si ancienneté < 1 an) """
        if not isinstance(value, list):
            raise serializers.ValidationError("Ce champ doit être un tableau (liste).")
        if len(value) > 12:
            raise serializers.ValidationError("Vous ne pouvez pas fournir plus de 12 mois de salaire.")
        # S'assure que chaque élément peut être converti en float (décimal)
        try:
            [float(salaire) for salaire in value]
        except ValueError:
            raise serializers.ValidationError("Tous les salaires dans le tableau doivent être des nombres.")
        return value
