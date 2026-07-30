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
        return CustomUser.objects.create_user(**validated_data)

    # NOUVEAU : Gérer la mise à jour (notamment du mot de passe)
    def update(self, instance, validated_data):
        # On extrait le mot de passe s'il est dans la requête
        password = validated_data.pop('password', None)
        
        # On met à jour les autres champs de manière classique
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Si un nouveau mot de passe a été fourni, on le hashe correctement
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance