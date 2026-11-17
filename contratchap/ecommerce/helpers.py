from django.db import transaction
from django.db.models import F

from .models import Cart, CartItem, Order, OrderItem, Coupon

def get_or_create_cart(request):
    # ─── Utilisateur authentifié ───
    if request.user.is_authenticated:
        # Récupère ou crée le panier de l'utilisateur (session_key forcé à None)
        user_cart, _ = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_key': None}
        )

        # Fusion avec un éventuel panier de session (invité)
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            try:
                session_cart = Cart.objects.get(id=session_cart_id, user__isnull=True)
                for item in session_cart.items.all():
                    existing_item = user_cart.items.filter(
                        contrat=item.contrat,
                        pro=item.pro,
                        customed_contract=item.customed_contract,
                        contract_revision=item.contract_revision,
                        packs=item.packs
                    ).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        CartItem.objects.create(
                            cart=user_cart,
                            contrat=item.contrat,
                            pro=item.pro,
                            customed_contract=item.customed_contract,
                            contract_revision=item.contract_revision,
                            packs=item.packs,
                            quantity=item.quantity,
                            unit_price=item.unit_price
                        )
                session_cart.delete()
                del request.session['cart_id']
            except Cart.DoesNotExist:
                pass

        return user_cart

    # ─── Utilisateur invité ───
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id, user__isnull=True)
            return cart
        except Cart.DoesNotExist:
            pass

    # Création ou récupération d'un panier invité avec une session_key valide
    if not request.session.session_key:
        request.session.create()          # génère une clé de session si absente
    
    # 🛠️ LA CORRECTION EST ICI : get_or_create au lieu de create !
    cart, created = Cart.objects.get_or_create(
        session_key=request.session.session_key,
        defaults={'user': None}
    )
    
    request.session['cart_id'] = str(cart.id)

    # Indique à set_cart_cookie_if_needed qu'il faut poser un cookie
    if created:
        request._new_cart_session_id = str(cart.id)
        
    return cart

def set_cart_cookie_if_needed(request, response):
    """
    Helper pour attacher le cookie 'cart_session_id' à la réponse 
    si un nouveau panier a été créé pour un invité.
    """
    if hasattr(request, '_new_cart_session_id'):
        response.set_cookie(
            key='cart_session_id',
            value=request._new_cart_session_id,
            httponly=True,  # Sécurisé contre les failles XSS
            max_age=30 * 24 * 60 * 60,  # Expire dans 30 jours
            samesite='Lax'
        )
    return response


def create_order_from_cart(
    request,
    cart,
    guest=None,
    order_status=Order.Status.PENDING,
    increment_coupon=True,
):
    """Snapshot a non-empty cart into an Order + OrderItems and clear the cart."""
    with transaction.atomic():
        subtotal = cart.get_total()
        final_total = cart.get_total_with_discount()
        discount = subtotal - final_total

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            guest=guest,
            status=order_status,
            total_amount=final_total,
            coupon=cart.coupon,
            discount_amount=discount,
        )

        if increment_coupon and order.coupon:
            Coupon.objects.filter(id=order.coupon.id).update(used_count=F('used_count') + 1)

        order_items = []
        for item in cart.items.select_related('contrat', 'pro', 'customed_contract', 'packs', 'contract_revision'):
            c_title = None
            p_name = None
            customized_name = None
            pack_title = None
            contract_revision = None
            revision_subject = None

            if item.contrat:
                c_title = item.contrat.title
            elif item.pro:
                pro_title = item.pro.get_title_display() if hasattr(item.pro, 'get_title_display') else getattr(item.pro, 'title', '')
                p_name = f"{item.pro.first_name} {item.pro.last_name} - {pro_title}"
            elif item.customed_contract:
                customized_name = item.customed_contract.subject or f"Contrat sur mesure #{item.customed_contract.id}"
            elif item.packs:
                pack_title = item.packs.title
            elif item.contract_revision:
                contract_revision = item.contract_revision
                revision_subject = item.contract_revision.subject or f"Révision #{item.contract_revision.id}"

            order_items.append(
                OrderItem(
                    order=order,
                    contrat=item.contrat,
                    pro=item.pro,
                    contrat_customed=item.customed_contract,
                    pack=item.packs,
                    contrat_title=c_title,
                    customised_contract=customized_name,
                    contract_revision=contract_revision,
                    pro_name=p_name,
                    pack_title=pack_title,
                    revision_subject=revision_subject,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                )
            )

        OrderItem.objects.bulk_create(order_items)
        cart.clear()
        return order