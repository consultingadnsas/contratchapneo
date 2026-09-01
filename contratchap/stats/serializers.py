from rest_framework import serializers
from .models import DailyVisit

class DailyVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyVisit
        fields = ['id', 'date', 'country', 'visits']