from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from .models import UserPack


class CreditError(Exception):
    """Levée quand l'utilisateur n'a plus de crédit disponible."""
    pass


CREDIT_FIELDS = {
    'contrat': 'credits_restants',      # contrats du catalogue
    'custom':  'customs_restants',      # contrats sur mesure
    'pro':     'cartes_pro_restantes',  # cartes de pro
}


def get_available_userpack(user, credit_type):
    """
    Retourne le UserPack valide (actif, non expiré) le plus proche de 
    l'expiration qui a encore du solde sur le crédit demandé.
    FIFO : on épuise en priorité les packs qui expirent bientôt.
    """
    field = CREDIT_FIELDS.get(credit_type)
    if not field:
        raise ValueError(f"Type de crédit inconnu : {credit_type}")

    return (
        UserPack.objects
        .filter(user=user, is_active=True)
        .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))
        .filter(**{f'{field}__gt': 0})
        .order_by('expires_at')
        .first()
    )


def consume_credit(user, credit_type):
    """
    LA GATE.
    Vérifie qu'il reste du crédit et le décrémente de façon atomique
    (select_for_update -> pas de race condition si double requête simultanée).
    Lève CreditError si aucun crédit dispo.
    Retourne le UserPack débité (utile pour lier contrats_choisis / pros_debloques).
    """
    field = CREDIT_FIELDS.get(credit_type)
    if not field:
        raise ValueError(f"Type de crédit inconnu : {credit_type}")

    with transaction.atomic():
        pack = (
            UserPack.objects
            .select_for_update()
            .filter(user=user, is_active=True)
            .filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))
            .filter(**{f'{field}__gt': 0})
            .order_by('expires_at')
            .first()
        )

        if not pack:
            raise CreditError(f"Aucun crédit '{credit_type}' disponible pour cet utilisateur.")

        setattr(pack, field, getattr(pack, field) - 1)
        pack.save(update_fields=[field])

    return pack