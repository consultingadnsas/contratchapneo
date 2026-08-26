from rest_framework import serializers
from .models import SimulationDroits

class SimulationDroitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulationDroits
        fields = '__all__'

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
