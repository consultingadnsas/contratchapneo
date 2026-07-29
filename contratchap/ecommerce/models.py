from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

# About relation
from contrat.models import (Contrat, CustomedContract, Pack)
from pro.models import LegalProfessional

class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Pourcentage (%)'
        FIXED = 'fixed', 'Montant fixe (FCFA)'

    code = models.CharField(max_length=50, unique=True, help_text="Ex: BIENTOT_AVOCAT_2026")
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valeur de la réduction")
    
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    max_usages = models.PositiveIntegerField(default=100, help_text="Combien de fois ce code peut-il être utilisé en tout ?")
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to and self.used_count < self.max_usages

class Cart(models.Model):
    """
        Panier hybride : lié à un user connecté OU à une session invité.
        Un seul des deux champs est renseigné à la fois.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Utilisateur connecté (optionnel)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        blank=True,
        null=True
    )

    # Invité — clé de session Django
    session_key = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        unique=True,
        help_text="Clé de session Django pour les invités"
    )

    # Code promo du panier
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False, session_key__isnull=True) |
                    models.Q(user__isnull=True, session_key__isnull=False)
                ),
                name='cart_user_or_session_exclusive' # 👈 Le nom correct pour le Cart
            )
        ]

    def __str__(self):
        if self.user:
            return f'Panier de {self.user}'
        return f'Panier invité (session {self.session_key[:8]}…)'

    @property
    def is_guest(self):
        return self.user is None

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def clear(self):
        self.items.all().delete()

    def merge_into_user_cart(self, user_cart):
        """
        Fusionne ce panier invité dans le panier d'un user qui vient de se connecter.
        Si le contrat existe déjà dans le panier user, on additionne les quantités.
        """
        for item in self.items.all():
            existing = user_cart.items.filter(contrat=item.contrat).first()
            if existing:
                existing.quantity += item.quantity
                existing.save()
            else:
                item.cart = user_cart
                item.save()
        self.delete()

    def get_total_with_discount(self):
        subtotal = self.get_total()
        if self.coupon and self.coupon.is_valid():
            if self.coupon.discount_type == 'percentage':
                discount = (self.coupon.discount_value / 100) * subtotal
                return subtotal - discount
            elif self.coupon.discount_type == 'fixed':
                return max(subtotal - self.coupon.discount_value, 0)
        return subtotal


class CartItem(models.Model):
    """
    Ligne du panier — hybride : peut contenir un Contrat OU un Professionnel.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    # Contrat devient optionnel
    contrat = models.ForeignKey(
        Contrat,
        on_delete=models.CASCADE,
        related_name='cart_items',
        null=True, 
        blank=True
    )
    # Pro devient optionnel
    pro = models.ForeignKey(
        LegalProfessional,
        on_delete=models.CASCADE,
        related_name='cart_items', # J'ai changé 'pro_items' en 'cart_items' pour la cohérence
        null=True, 
        blank=True
    )
    # Contrat sur demande devient optionnel
    customed_contract = models.ForeignKey(
        CustomedContract,
        on_delete=models.CASCADE,
        related_name='customed_contract_items',
        null=True,
        blank=True
    )
    # Packs de contrats
    packs = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        related_name='packs_items',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Snapshot du prix au moment de l'ajout"
    )

    user_inputs = models.JSONField(
        default=dict,
        blank=True, 
        null = True,
        help_text='Stock les variables saisies par le client pour générer le contrat'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(contrat__isnull=False, pro__isnull=True, customed_contract__isnull=True, packs__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=False, customed_contract__isnull=True, packs__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=True, customed_contract__isnull=False, packs__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=True, customed_contract__isnull=True, packs__isnull=False)
                ),
                name='cartitem_exclusive_type' # 👈 Le nom correct pour le CartItem
            )
        ]

    def __str__(self):
        if self.contrat:
            return f'{self.quantity}x Contrat : {self.contrat.title}'
        elif self.customed_contract:
            return f'{self.quantity}x Sur mesure : {self.customed_contract.subject}'
        elif self.pro:
            # 💡 Astuce : get_title_display() affichera "Avocat" au lieu de "AVOCAT"
            return f'{self.quantity}x Pro : {self.pro.get_title_display()} {self.pro.last_name}'
        elif self.packs:
            # Assure-toi que ton modèle Pack a bien un champ 'title' ou 'name'
            return f'{self.quantity}x Pack : {self.packs.title}' 
            
        return f'{self.quantity}x Élément inconnu'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            if self.contrat:
                self.unit_price = self.contrat.prix
            elif self.customed_contract:
                # 💡 Assure-toi que CustomedContract possède bien un champ 'prix'
                self.unit_price = self.customed_contract.prix 
            elif self.pro:
                self.unit_price = self.pro.prix
            elif self.packs:
                self.unit_price = self.packs.prix
        super().save(*args, **kwargs)

class GuestInfo(models.Model):
    """
    Infos de l'invité collectées au checkout.
    Lié à la commande (Order) — pas au panier.
    Permet d'envoyer le lien de téléchargement par email.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} ({self.email})'
    
class Order(models.Model):

    class Status(models.TextChoices):
        PENDING   = 'pending',   'En attente de paiement'
        PAID      = 'paid',      'Payé'
        CANCELLED = 'cancelled', 'Annulé'
        REFUNDED  = 'refunded',  'Remboursé'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Acheteur — user connecté OU invité, jamais les deux
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True
    )
    guest = models.OneToOneField(
        'GuestInfo',
        on_delete=models.SET_NULL,
        related_name='order',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Snapshot du total au moment du checkout
    # Ne pas recalculer depuis les OrderItems après coup —
    # les prix peuvent avoir changé
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    download_count = models.PositiveIntegerField(
        default=0, 
        help_text="Nombre de fois que l'acheteur a télécharger le contrat"
    )

    # Code pour la réduction
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Montant exact déduit via le coupon"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            # Même logique que Cart : user OU guest, exclusif
            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False, guest__isnull=True) |
                    models.Q(user__isnull=True,  guest__isnull=False)
                ),
                name='order_user_or_guest_exclusive'
            )
        ]

    def __str__(self):
        owner = self.user or self.guest
        return f'Commande {str(self.id)[:8]}… — {owner} — {self.get_status_display()}'

    @property
    def is_guest_order(self):
        return self.guest is not None

    @property
    def buyer_email(self):
        """Retourne l'email de l'acheteur quel que soit son type."""
        if self.user:
            return self.user.email
        return self.guest.email

    def get_total_from_items(self):
        """Recalcul depuis les lignes — utile pour vérification/audit."""
        return sum(item.get_subtotal() for item in self.order_items.all())

    def can_be_cancelled(self):
        return self.status == self.Status.PENDING


class OrderItem(models.Model):
    """
    Ligne de commande — snapshot complet au moment du checkout.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    contrat = models.ForeignKey(
        'contrat.Contrat',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='order_items'
    )
    pro = models.ForeignKey(
        'pro.LegalProfessional',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='order_items'
    )
    contrat_customed = models.ForeignKey(
        'contrat.CustomedContract',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    pack = models.ForeignKey(
        'contrat.Pack',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='order_items'
    )

    # Snapshots — figés définitivement au moment du checkout
    # Rendu optionnel selon ce qu'on achète
    contrat_title = models.CharField(max_length=255, null=True, blank=True)
    customised_contract = models.CharField(max_length=225, null=True, blank=True)
    pro_name = models.CharField(max_length=255, null=True, blank=True) 
    pack_title = models.CharField(max_length=255, null=True, blank=True)
    user_inputs = models.JSONField(
        default=dict,
        blank=True, 
        null = True,
        help_text='Stock les variables saisies par le client pour générer le contrat'
    )

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(contrat__isnull=False, pro__isnull=True, contrat_customed__isnull=True, pack__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=False, contrat_customed__isnull=True, pack__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=True, contrat_customed__isnull=False, pack__isnull=True) |
                    models.Q(contrat__isnull=True, pro__isnull=True, contrat_customed__isnull=True, pack__isnull=False)
                ),
                name='orderitem_exclusive_type' # 👈 Le nom correct pour l'OrderItem
            )
        ]

    def __str__(self):
        if self.contrat_title:
            name = self.contrat_title
        elif self.customised_contract:
            name = f"Sur mesure : {self.customised_contract}"
        elif self.pack_title:
            name = f"Pack : {self.pack_title}"
        else:
            name = f"Carte - {self.pro_name}"
        return f'{self.quantity} x {name} — commande {str(self.order.id)[:8]}…'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs): 
        if not self.contrat_title and self.contrat:
            self.contrat_title = self.contrat.title
        if not self.pro_name and self.pro:
            self.pro_name = f"{self.pro.first_name} {self.pro.last_name}"
        if not self.customised_contract and self.contrat_customed:
            self.customised_contract = getattr(self.contrat_customed, 'title', f"Demande sur mesure #{self.contrat_customed.id}")
        
        # NOUVEAU : Capture du nom du pack
        if not self.pack_title and self.pack:
            self.pack_title = self.pack.title
            
        super().save(*args, **kwargs)
