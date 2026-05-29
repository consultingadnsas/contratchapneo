from django.db import models
from django.conf import settings
import uuid

# About relation
from contrat.models import Contrat

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

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Un panier doit avoir soit un user, soit une session_key — pas les deux
            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False, session_key__isnull=True) |
                    models.Q(user__isnull=True, session_key__isnull=False)
                ),
                name='cart_user_or_session_exclusive'
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


class CartItem(models.Model):
    """
    Ligne du panier — identique pour user et invité.
    unit_price est un snapshot du prix au moment de l'ajout.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    contrat = models.ForeignKey(
        Contrat,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Snapshot du prix au moment de l'ajout"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'contrat')

    def __str__(self):
        return f'{self.quantity}x {self.contrat.title}'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.contrat.prix
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
    Même logique que CartItem mais immuable une fois créé.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    contrat = models.ForeignKey(
        'contrat.Contrat',
        on_delete=models.SET_NULL,   # Si le contrat est supprimé,
        null=True,                   # la commande reste intacte
        related_name='order_items'
    )

    # Snapshots — figés définitivement au moment du checkout
    contrat_title = models.CharField(max_length=255)   # garde le titre même si contrat supprimé
    unit_price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity      = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'contrat')

    def __str__(self):
        return f'{self.quantity}x {self.contrat_title} — commande {str(self.order.id)[:8]}…'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        # Snapshot automatique du titre si pas encore défini
        if not self.contrat_title and self.contrat:
            self.contrat_title = self.contrat.title
        super().save(*args, **kwargs)