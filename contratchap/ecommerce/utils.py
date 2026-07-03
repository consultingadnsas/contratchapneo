import io
import zipfile
from django.http import FileResponse
from django.core.mail import send_mail
from ecommerce.models import Order
from django.conf    import settings
from django.db.models import F

from contrat.models import Contrat
from .models import Order, OrderItem

def _send_download_email(order: Order):
    """
    Envoie le lien de téléchargement après paiement confirmé.

    - User connecté → lien simple (il s'auth lui-même)
    - Invité        → lien avec ?email= (order.guest.email via order.buyer_email)
    """
    buyer_email   = order.buyer_email          # property sur Order — user ou guest
    base_url      = settings.FRONTEND_URL.rstrip('/')
    download_path = f'/payment/download/{order.id}/'

    if order.guest:
        download_url = f'{base_url}{download_path}?email={buyer_email}'
    else:
        download_url = f'{base_url}{download_path}'

    # contrat_title est un snapshot — toujours présent même si le contrat est supprimé
    titres     = [item.contrat_title for item in order.order_items.all()]
    titres_str = '\n'.join(f'  • {t}' for t in titres)

    send_mail(
        subject   = '✅ Paiement confirmé — Vos contrats sont disponibles',
        message   = (
            f'Bonjour,\n\n'
            f'Votre paiement de {order.total_amount} FCFA a été validé.\n\n'
            f'Contrat(s) acheté(s) :\n{titres_str}\n\n'
            f'Téléchargez-les ici :\n{download_url}\n\n'
            f'Merci pour votre confiance.'
        ),
        from_email    = settings.DEFAULT_FROM_EMAIL,
        recipient_list= [buyer_email],
        fail_silently = False,
    ) 

def stream_single_pdf(file_field, filename:str) -> FileResponse:
    """"
        Stream n'import quel fichier (contrat ou carte de visite)
    """
    response = FileResponse(
        file_field.open('rb'),
        content_type='application/pdf'
    )
    # Assainir le nom du fichier (retirer les espaces pour éviter les bugs dans le navigateur)
    safe_filename = filename.replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}.pdf"'
    return response
