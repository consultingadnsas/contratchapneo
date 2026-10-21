from django.utils import timezone
from rest_framework import serializers
from .models import Consulting


class ConsultingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulting
        fields = [
            "id", "title", "full_name", "email", "description",
            "meet_day", "consulting_hour", "status",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def validate_meet_day(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError(
                "Impossible de réserver à une date passée."
            )
        return value