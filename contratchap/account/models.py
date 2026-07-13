from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import uuid
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