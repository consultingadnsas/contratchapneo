from rest_framework import serializers
from .models import Cart, CartItem, GuestInfo, Order, OrderItem
from contrat.models import Contrat


# ─────────────────────────────────────────
# CONTRAT (lecture seule — cross-app)
# ─────────────────────────────────────────

class ContratMiniSerializer(serializers.ModelSerializer):
    """
    Représentation légère du Contrat pour l'affichage dans le panier.
    On n'importe que ce dont le frontend a besoin.
    """
    class Meta:
        model = Contrat
        fields = [
            'id', 
            'title', 
            'prix', 
            'picture'
        ]


# ─────────────────────────────────────────
# CART
# ─────────────────────────────────────────

class CartItemSerializer(serializers.ModelSerializer):
    contrat         = ContratMiniSerializer(read_only=True)
    contrat_id      = serializers.UUIDField(write_only=True)
    subtotal        = serializers.SerializerMethodField()

    class Meta:
        model  = CartItem
        fields = [
            'id',
            'contrat',       # lecture — objet complet
            'contrat_id',    # écriture — UUID uniquement
            'quantity',
            'unit_price',
            'subtotal',
            'created_at',
        ]
        read_only_fields = ['id', 'unit_price', 'created_at']

    def get_subtotal(self, obj):
        return obj.get_subtotal()

    def validate_contrat_id(self, value):
        try:
            Contrat.objects.get(id=value)
        except Contrat.DoesNotExist:
            raise serializers.ValidationError("Ce contrat n'existe pas.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("La quantité doit être au moins 1.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items    = CartItemSerializer(many=True, read_only=True)
    total    = serializers.SerializerMethodField()
    is_guest = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Cart
        fields = [
            'id',
            'is_guest',
            'items',
            'total',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.get_total()


# ─────────────────────────────────────────
# GUEST INFO
# ─────────────────────────────────────────

class GuestInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model  = GuestInfo
        fields = ['id', 'email', 'full_name', 'phone_number']
        read_only_fields = ['id']

    def validate_email(self, value):
        return value.lower().strip()

    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Le nom complet est trop court.")
        return value.strip()

    def validate_phone_number(self, value):
        import re
        cleaned = re.sub(r'\s+', '', value.strip())
        # Accepte les formats : +2250101010101, 0101010101, 01 01 01 01 01
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError(
                "Numéro de téléphone invalide. Formats acceptés : +2250701234567 ou 0701234567."
            )
        return cleaned


# ─────────────────────────────────────────
# ORDER
# ─────────────────────────────────────────

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model  = OrderItem
        fields = [
            'id',
            'contrat',        # FK (peut être null si contrat supprimé)
            'contrat_title',  # snapshot — toujours présent
            'unit_price',
            'quantity',
            'subtotal',
        ]
        read_only_fields = fields

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    order_items  = OrderItemSerializer(many=True, read_only=True)
    status_label = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    buyer_email  = serializers.EmailField(read_only=True)

    class Meta:
        model  = Order
        fields = [
            'id',
            'status',
            'status_label',
            'total_amount',
            'buyer_email',
            'order_items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer dédié au checkout.
    Valide les infos guest si l'utilisateur n'est pas connecté.
    """
    guest = GuestInfoSerializer(required=False)

    def validate(self, data):
        request = self.context.get('request')

        # Si l'utilisateur n'est pas connecté, les infos guest sont obligatoires
        if not request.user.is_authenticated:
            if not data.get('guest'):
                raise serializers.ValidationError({
                    'guest': "Les informations invité sont obligatoires pour un achat sans compte."
                })
        return data