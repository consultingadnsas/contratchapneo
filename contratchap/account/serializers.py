from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'phone_number',
            'user_type',
            'first_name',
            'last_name',
        ]
        read_only_fields = ['id']

        def validate(self, data):
            if CustomUser.objects.filter(username=data.get('username', '')).exists():
                raise serializers.ValidationError(
                    {'username': _("Ce nom d'utilisateur est déjà pris")}
                )
            if CustomUser.objects.filter(email=data.get('email', '')).exists():
                raise serializers.ValidationError(
                    {'email': _("Cet email est déjà utilisé")}
                )
            return data
        
        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            return user