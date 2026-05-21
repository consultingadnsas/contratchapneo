from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number', 
            'user_type', 'first_name', 'last_name', 'password'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # create_user se charge de hasher le mot de passe proprement
        return CustomUser.objects.create_user(**validated_data)