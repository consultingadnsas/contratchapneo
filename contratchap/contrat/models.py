from django.db import models
from django.conf import settings
import uuid
from account.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from pro.models import LegalProfessional
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
    
class Pack(models.Model):

    """ 
        LE CATALOGUE (Ce qui s'affiche sur la boutique) 
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    # 🚀 NOUVEAU : Le mode "Crédits"
    nombre_credits = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de contrats au choix que l'utilisateur pourra débloquer gratuitement."
    )
    
    # 1. Contrats fixes inclus d'office (Le mode "Bundle" classique)
    contrats = models.ManyToManyField(
        Contrat,
        related_name='packs',
        blank=True,
        help_text="Les contrats spécifiques inclus d'office dans ce pack."
    )

    # 🎁 NOUVEAU : Autres Avantages (Exemples très demandés en LégalTech)
    custom_contract_included = models.BooleanField(
        default=False,
        help_text="Inclusion des contrats sur mesure"
    )

    nombre_customed_contract = models.IntegerField(
        default=0,
        help_text="Nombre de contrat personnalisé"
    )

    consultation_pro_incluse = models.BooleanField(
        default=False,
        help_text="Cochez si ce pack offre une mise en relation/consultation gratuite avec un pro."
    )

    nombre_cartes_pro = models.PositiveIntegerField(
        default=1,
        help_text="Nombre de cartes de visite de professionnels téléchargeables avec ce pack (1 pour le pack Basique, plus pour les offres supérieures)."
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
    
    # 💰 NOUVEAU : Le solde de crédits pour les contrats
    credits_restants = models.PositiveIntegerField(
        default=0,
        help_text="Combien de crédits il reste à l'utilisateur pour ce pack."
    )
    
    # NOUVEAU : Historique des choix
    contrats_choisis = models.ManyToManyField(
        Contrat, 
        blank=True, 
        help_text="Les contrats que l'utilisateur a choisi de débloquer avec ses crédits."
    )

    cartes_pro_restantes = models.PositiveIntegerField(
        default=0,
        help_text="Combien de cartes de pro il reste à télécharger pour ce pack."
    )

    # Pour les crédits restant des contrats sur mesure
    customs_restants = models.PositiveIntegerField(
        default=0,
        help_text="Nombre de contrats sur mesure restants à utiliser pour ce pack."
    )

    pros_debloques = models.ManyToManyField(
        LegalProfessional,  # adapte le chemin selon ton app
        blank=True,
        related_name='debloque_par',
        help_text="Les professionnels dont la carte a déjà été débloquée avec ce pack."
    )

    is_active = models.BooleanField(default=True) 
    expires_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.pack.title} ({self.credits_restants} crédits restants)'

    def save(self, *args, **kwargs):
        # 🚨 CORRECTION ICI : self._state.adding garantit que c'est une création
        if self._state.adding: 
            self.credits_restants = self.pack.nombre_credits
            self.cartes_pro_restantes = self.pack.nombre_cartes_pro
            self.customs_restants = self.pack.nombre_customed_contract
            
            if self.pack.duree_validite_jours:
                from datetime import timedelta
                from django.utils import timezone
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

class CustomedContract(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='customised_contracts'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='customed_contracts'
    )
    # 🆕 Lien vers le pack utilisé pour débloquer cette demande
    user_pack = models.ForeignKey(
        UserPack,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='customed_contracts'
    )
    subject = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    description = models.TextField()
    #
    price = models.FloatField(default=25000.00)
    promo_price = models.FloatField(default=0.0)

    final_document = models.FileField(
        upload_to='customed_contracts/completed/',
        blank=True,
        null=True,
        help_text="PDF final rédigé, uploadé par le juriste une fois terminé."
    )
    is_wrotten = models.BooleanField(default = False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Contrat sur mesure de {self.email}'

class ContractRevision(models.Model):
    
    class RevisionStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        IN_PROGRESS = 'IN_PROGRESS', 'En cours de révision'
        COMPLETED = 'COMPLETED', 'Terminé'
        REJECTED = 'REJECTED', 'Rejeté / Annulé'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # --- Relations ---
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Plus sûr que CustomUser directement si tu changes d'avis plus tard
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='contract_revisions'
    )
    
    # S'il utilise un pack pour payer cette révision
    user_pack = models.ForeignKey(
        UserPack,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='contract_revisions'
    )

    # --- Informations sur la demande ---
    subject = models.CharField(max_length=225, help_text="Titre ou nature du contrat à réviser")
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    client_instructions = models.TextField(help_text="Ce que le client souhaite que vous vérifiiez spécifiquement")
    
    # --- Les Fichiers ---
    original_file = models.FileField(
        upload_to='revisions/originals/', 
        help_text="Le contrat envoyé par le client"
    )
    revised_file = models.FileField(
        upload_to='revisions/completed/', 
        blank=True, 
        null=True, 
        help_text="Le contrat révisé et renvoyé par vos juristes"
    )
    
    # --- Tarification ---
    price = models.FloatField(default=15000.00)
    promo_price = models.FloatField(default=0.0)

    # --- Suivi et Statut ---
    status = models.CharField(
        max_length=20,
        choices=RevisionStatus.choices,
        default=RevisionStatus.PENDING
    )
    is_revised = models.BooleanField(default=False)
    
    # Commentaires internes ou pour le client
    expert_comments = models.TextField(blank=True, null=True, help_text="Notes laissées par le juriste après révision")

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Révision: {self.subject} - {self.email} ({self.get_status_display()})'