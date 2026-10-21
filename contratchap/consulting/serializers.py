from django.utils import timezone
from rest_framework import serializers
from .models import Consulting


class ConsultingSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Consulting
        fields = [
            "id", "title", "full_name", "phone_number", "email", "description",
            "meet_day", "consulting_hour", "status", "status_display",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status_display", "created_at", "updated_at"]

    def to_internal_value(self, data):
        # Supporte à la fois "09:30", "09:30:00" et le format frontend "09h30"
        if isinstance(data, dict) and 'consulting_hour' in data:
            hour_val = data.get('consulting_hour')
            if isinstance(hour_val, str) and 'h' in hour_val.lower():
                parts = hour_val.lower().split('h')
                if len(parts) == 2:
                    data = data.copy()
                    data['consulting_hour'] = f"{parts[0].strip().zfill(2)}:{parts[1].strip().zfill(2)}:00"
        return super().to_internal_value(data)

    def validate_meet_day(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError(
                "Impossible de réserver à une date passée."
            )
        # Vérifier que ce n'est pas un samedi ou un dimanche
        if value.weekday() in [5, 6]:
            raise serializers.ValidationError(
                "Les rendez-vous ont lieu du lundi au vendredi uniquement."
            )
        return value

    def validate(self, attrs):
        meet_day = attrs.get('meet_day')
        consulting_hour = attrs.get('consulting_hour')

        # Si le rendez-vous est pour aujourd'hui, vérifier que l'heure n'est pas déjà passée
        if meet_day == timezone.localdate() and consulting_hour:
            if consulting_hour < timezone.localtime().time():
                raise serializers.ValidationError(
                    {"consulting_hour": "Ce créneau horaire est déjà passé pour aujourd'hui."}
                )

        # Vérification d'un créneau déjà pris
        instance = getattr(self, 'instance', None)
        if meet_day and consulting_hour:
            qs = Consulting.objects.filter(meet_day=meet_day, consulting_hour=consulting_hour)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"detail": "Ce créneau horaire vient d'être réservé. Veuillez choisir un autre horaire."}
                )

        return attrs