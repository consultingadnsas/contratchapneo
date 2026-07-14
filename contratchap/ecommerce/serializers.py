from rest_framework import serializers
from .models import Cart, CartItem, GuestInfo, Order, OrderItem
from contrat.models import Contrat, CustomedContract, Pack, UserPack
from pro.models import LegalProfessional 

# ─────────────────────────────────────────
# MINI SERIALIZERS (lecture seule — affichage panier)
# ─────────────────────────────────────────

class ContratMiniSerializer(serializers.ModelSerializer):
    """ Représentation légère du Contrat """
    class Meta:
        model = Contrat
        fields = [
            'id', 
            'title', 
            'prix', 
            'picture'
        ]

class ProMiniSerializer(serializers.ModelSerializer):
    """ Représentation légère du Pro pour l'affichage dans le panier """
    title_display = serializers.CharField(source='get_title_display', read_only=True)
    
    class Meta:
        model = LegalProfessional
        # On renvoie l'essentiel pour afficher la "carte" dans le panier Nuxt
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'title_display', 
            'prix', 
            'profile_picture'
        ]

class CustomizedContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomedContract
        fields = [
            'id',
            'subject',
            'phone_number',
            'email',
            'description',
            'price',
            'is_wrotten'
        ]

# 🚨 CORRECTION 1 : ModelSerializer au lieu de ModelField
class PackMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        fields = [
            'id',
            'title',
            'description',
            'prix',
            'contrats',
            'picture' # Assure-toi que c'est bien le nom exact dans ton model Pack (pic ou picture)
        ]


# ─────────────────────────────────────────
# GESTION DE L'AJOUT AU PANIER (Écriture)
# ─────────────────────────────────────────

class AddToCartSerializer(serializers.Serializer):
    """
    Sérialiseur dédié UNIQUEMENT à l'action POST /cart/add/.
    Valide qu'on ajoute soit un contrat, soit un pro, soit un sur-mesure, SOIT un pack.
    """
    contrat_id = serializers.UUIDField(required=False, allow_null=True)
    pro_id = serializers.UUIDField(required=False, allow_null=True) 
    customed_contract = serializers.UUIDField(required=False, allow_null=True)
    pack_id = serializers.UUIDField(required=False, allow_null=True) # ✅
    quantity = serializers.IntegerField(default=1, min_value=1)

    def validate(self, data):
        contrat_id = data.get('contrat_id')
        pro_id = data.get('pro_id')
        customed_contract = data.get('customed_contract')
        pack_id = data.get('pack_id')

        # On compte combien de champs sont remplis (le Pack est inclus)
        provided_items = sum(x is not None for x in [contrat_id, pro_id, customed_contract, pack_id])

        # Vérification stricte : un seul article à la fois !
        if provided_items > 1:
            raise serializers.ValidationError("Vous ne pouvez pas ajouter plus d'un type d'article en même temps.")
        if provided_items == 0:
            raise serializers.ValidationError("Vous devez fournir soit un contrat_id, soit un pro_id, soit un customed_contract, soit un pack_id.")

        # Vérification de l'existence en Base de Données
        if contrat_id and not Contrat.objects.filter(id=contrat_id).exists():
            raise serializers.ValidationError({"contrat_id": "Ce contrat n'existe pas."})
        if pro_id and not LegalProfessional.objects.filter(id=pro_id).exists():
            raise serializers.ValidationError({"pro_id": "Ce professionnel n'existe pas."})
        if customed_contract and not CustomedContract.objects.filter(id=customed_contract).exists():
            raise serializers.ValidationError({"customed_contract": "Ce contrat sur mesure n'existe pas."})
        if pack_id and not Pack.objects.filter(id=pack_id).exists():
            raise serializers.ValidationError({"pack_id": "Ce pack n'existe pas."})

        return data


# ─────────────────────────────────────────
# CART (Lecture)
# ─────────────────────────────────────────

class CartItemSerializer(serializers.ModelSerializer):
    contrat = ContratMiniSerializer(read_only=True)
    pro = ProMiniSerializer(read_only=True)
    customed_contract = CustomizedContractSerializer(read_only=True)
    # CORRECTION ICI : On mappe le champ "packs" du modèle vers la clé "pack" de l'API
    pack = PackMiniSerializer(source='packs', read_only=True) 
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'contrat',           
            'pro',               
            'customed_contract', 
            'pack',              
            'quantity',
            'user_inputs',
            'unit_price',
            'subtotal',
            'created_at',
        ]
        read_only_fields = ['id', 'unit_price', 'created_at']

    def get_subtotal(self, obj):
        return obj.get_subtotal()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    is_guest = serializers.BooleanField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'is_guest',
            'items',
            'total',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at'
        ]

    def get_total(self, obj):
        return obj.get_total()


# ─────────────────────────────────────────
# GUEST INFO
# ─────────────────────────────────────────

class GuestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = GuestInfo
        fields = [
            'id', 
            'email', 
            'full_name', 
            'phone_number'
        ]
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
            'contrat',              # FK
            'contrat_title',        # snapshot 
            'pro',                  # FK
            'pro_name',             # snapshot 
            'contrat_customed',     # FK
            'customised_contract',  # snapshot 
            'pack',                 # 🚨 CORRECTION 2 : NOUVEAU FK (Tu l'avais oublié)
            'pack_title',           # 🚨 CORRECTION 2 : NOUVEAU snapshot (Tu l'avais oublié)
            'unit_price',
            'user_inputs',
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
    guest = GuestInfoSerializer(required=False)

    def validate(self, data):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            if not data.get('guest'):
                raise serializers.ValidationError({
                    'guest': "Les informations invité sont obligatoires pour un achat sans compte."
                })
        return data