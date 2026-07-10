from django.db import models
from django.conf import settings
import uuid
from account.models import CustomUser
# Create your models here.

class Category(models.Model):

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'la catégorie {self.title}'
    
class Contrat(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, # <- La sécurité est ici
        blank=True, 
        null=True, 
        related_name='contrats'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Media About the contrat
    fichier_modele = models.FileField(upload_to='modeles/')
    picture = models.ImageField(upload_to='contrat_images/', blank=True, null=True)

    # Statistics
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    # Visibility
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Contrat {self.title}'

class CustomedContract(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='customised_contracts'
    )
    subject = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    description = models.TextField()
    #
    price = models.FloatField(default=25000.00)
    promo_price = models.FloatField(default=0.0)

    is_wrotten = models.BooleanField(default = False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Contrat sur mesure de {self.email}'

    
class Pack(models.Model):
    """ LE CATALOGUE (Ce qui s'affiche sur la boutique) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    
    contrats = models.ManyToManyField(
        Contrat,
        related_name='packs',
        blank=True
    )
    picture = models.ImageField(upload_to='pack_images/', blank=True, null=True)

    # Statistics
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)

    # Visibility sur la boutique
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pack {self.title} ({self.contrats.count()} contrats)'


class UserPack(models.Model):
    """ L'ACHAT (Ce qui donne le droit d'accès gratuit à l'utilisateur) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Qui a acheté ?
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mes_packs')
    
    # Qu'est-ce qu'il a acheté ?
    pack = models.ForeignKey(Pack, on_delete=models.PROTECT, related_name='purchasers')
    
    # Est-ce que son pack est toujours valide ?
    is_active = models.BooleanField(default=True) 
    
    # Optionnel : Tu pourrais ajouter une date d'expiration si le pack dure 1 an par exemple
    # expires_at = models.DateTimeField(null=True, blank=True)

    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} a acheté le {self.pack.title}'