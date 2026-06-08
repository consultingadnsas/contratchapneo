from .models import Cart

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def get_or_create_cart(request):
    """
    Retourne le panier existant ou en crée un nouveau.
    - User connecté  → panier lié au user
    - Invité         → panier lié à la session Django
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    # Crée la session si elle n'existe pas encore
    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
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