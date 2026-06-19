from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du pays")
    code = models.CharField(max_length=5, unique=True, help_text="Code ISO (ex: CI, SN, CM)")
    is_ohada_member = models.BooleanField(default=True, verbose_name="Membre de l'espace OHADA")
    
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"
        ordering = ['name']

    def __str__(self):
        return self.name

class LegalDomain(models.Model):
    # Idéal pour lister les Actes Uniformes : Droit des Sociétés (AUSCGIE), Droit Commercial Général (AUDCG), Sûretés, etc.
    name = models.CharField(max_length=150, unique=True, verbose_name="Domaine d'expertise")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Domaine du droit (ou Acte Uniforme)"
        verbose_name_plural = "Domaines du droit"
        ordering = ['name']

    def __str__(self):
        return self.name

class LegalProfessional(models.Model):
    TITLE_CHOICES = (
        ('AVOCAT', 'Avocat'),
        ('NOTAIRE', 'Notaire'),
        ('CONSEIL_JURIDIQUE', 'Conseil Juridique et Fiscal'),
        ('JURISTE', 'Juriste d\'entreprise'),
        ('HUISSIER', 'Huissier de justice'),
        ('MANDATAIRE', 'Mandataire Judiciaire / Syndic'), # Très important pour les procédures collectives OHADA
        ('EXPERT_COMPTABLE', 'Expert-Comptable / Commissaire aux comptes'), # Souvent sollicités pour la création de SARL/SA
        ('AUTRE', 'Autre professionnel du droit'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom de famille")
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, verbose_name="Titre professionnel")
    
    # Preuve de légitimité (Très important dans l'espace OHADA)
    professional_order = models.CharField(max_length=150, blank=True, null=True, help_text="Ex: Barreau de Côte d'Ivoire, Ordre des Notaires du Sénégal...")
    registration_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numéro d'inscription à l'ordre")
    
    # Contact
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    website = models.URLField(blank=True, null=True, verbose_name="Site web / LinkedIn")
    
    # Présentation
    profile_picture = models.ImageField(upload_to='professionals/profiles/', null=True, blank=True, verbose_name="Photo de profil")
    bio = models.TextField(verbose_name="Biographie / Présentation")
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name="Années d'expérience")
    
    # Localisation et Spécialités
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='professionals', verbose_name="Pays d'exercice")
    city = models.CharField(max_length=100, verbose_name="Ville d'exercice (ex: Abidjan, Dakar, Douala)")
    domains = models.ManyToManyField(LegalDomain, related_name='professionals', verbose_name="Domaines d'expertise (Actes Uniformes, etc.)")
    
    is_active = models.BooleanField(default=True, verbose_name="Profil actif")
    is_verified = models.BooleanField(default=False, help_text="Cocher si Contratchap a vérifié l'identité et l'inscription à l'ordre de ce professionnel.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professionnel de l'espace OHADA"
        verbose_name_plural = "Professionnels de l'espace OHADA"
        ordering = ['-is_verified', '-created_at'] # Met les profils vérifiés en premier !

    def __str__(self):
        return f"{self.get_title_display()} {self.first_name} {self.last_name}"