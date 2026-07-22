from django.db import models
from django.conf import settings
import uuid
from account.models import CustomUser
from django.utils import timezone
from datetime import timedelta
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
    
    # 1. Contrats fixes inclus d'office (Le mode "Bundle" classique)
    contrats = models.ManyToManyField(
        Contrat,
        related_name='packs',
        blank=True,
        help_text="Les contrats spécifiques inclus d'office dans ce pack."
    )
    
    # 🚀 NOUVEAU : Le mode "Crédits"
    nombre_credits = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de contrats au choix que l'utilisateur pourra débloquer gratuitement."
    )

    # 🎁 NOUVEAU : Autres Avantages (Exemples très demandés en LégalTech)
    remise_sur_mesure = models.PositiveIntegerField(
        default=0,
        help_text="Pourcentage de réduction sur les requêtes 'CustomedContract' (ex: 20 pour 20%)"
    )
    consultation_pro_incluse = models.BooleanField(
        default=False,
        help_text="Cochez si ce pack offre une mise en relation/consultation gratuite avec un pro."
    )
    duree_validite_jours = models.PositiveIntegerField(
        default=365,
        help_text="Durée de validité du pack en jours (ex: 365 pour 1 an)."
    )

    picture = models.ImageField(upload_to='pack_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Pack {self.title} ({self.contrats.count()} fixes, {self.nombre_credits} crédits)'


class UserPack(models.Model):
    """ L'ACHAT (Le portefeuille de l'utilisateur) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mes_packs')
    pack = models.ForeignKey(Pack, on_delete=models.PROTECT, related_name='purchasers')
    
    # 💰 NOUVEAU : Le solde de crédits
    credits_restants = models.PositiveIntegerField(
        default=0,
        help_text="Combien de crédits il reste à l'utilisateur pour ce pack."
    )
    
    # 🗂️ NOUVEAU : Historique des choix
    contrats_choisis = models.ManyToManyField(
        Contrat, 
        blank=True, 
        help_text="Les contrats que l'utilisateur a choisi de débloquer avec ses crédits."
    )

    is_active = models.BooleanField(default=True) 
    expires_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.pack.title} ({self.credits_restants} crédits restants)'

    def save(self, *args, **kwargs):
        # Initialisation automatique lors de la création (achat du pack)
        if not self.pk: 
            # On copie le nombre de crédits initiaux du catalogue
            self.credits_restants = self.pack.nombre_credits
            
            # On calcule la date d'expiration
            if self.pack.duree_validite_jours:
                self.expires_at = timezone.now() + timedelta(days=self.pack.duree_validite_jours)
                
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        """ Vérifie si le pack est toujours valide (actif et non expiré) """
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True