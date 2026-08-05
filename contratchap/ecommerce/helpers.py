from .models import Cart, CartItem

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