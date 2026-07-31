from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class CustomUser(AbstractUser):

    class USER_TYPE(models.TextChoices):
        ENTREPRISE = 'ENTREPRISE', _('Entreprise')
        INDIVIDUAL = 'INDIVIDUAL', _('Individual')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE.choices, default=USER_TYPE.INDIVIDUAL)

    # About subscription
    def __str__(self):
        return f'le profile de {self.username}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    @classmethod
    def create_token(cls, user, expiration_hours=24):
        """Méthode utilitaire pour créer un token avec expiration"""
        token = cls(
            user=user,
            expires_at=timezone.now() + timedelta(hours=expiration_hours)
        )
        token.save()
        return token
    
    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f'Token for {self.user.username}'