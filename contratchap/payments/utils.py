import io
import zipfile
from django.http import FileResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F

from contrat.models import Contrat, Pack
from ecommerce.models import Order

# --- Fichier PDF Unique Générique ---
def stream_single_pdf(file_field, filename: str) -> FileResponse:
    """
    Streame n'importe quel fichier (contrat ou carte de visite) directement en PDF.
    """
    response = FileResponse(
        file_field.open('rb'),
        content_type='application/pdf'
    )
    # Assainir le nom du fichier (retirer les espaces pour éviter les bugs navigateurs)
    safe_filename = filename.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{safe_filename}.pdf"'
    return response

# --- ZIP Mixte (Contrats PDF + Cartes de visite PDF) ---
def stream_zip(contrats: list, pros: list, order_id) -> FileResponse:
    """
    Zippe les fichiers modèles (contrats) et les cartes de visite (PDF) ensemble.
    """
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        
        # 1. Ajouter les contrats
        for contrat in contrats:
            zf.writestr(f'{contrat.title.replace(" ", "_")}.pdf', contrat.fichier_modele.read())
        
        # 2. Ajouter les cartes de visite (PDFs)
        for pro in pros:
            # On suppose que ton modèle pro a un champ `carte_visite` (FileField)
            if pro.carte_visite: 
                nom_fichier = f"Contact_{pro.user.first_name}_{pro.user.last_name}.pdf" if pro.user else "Contact_Pro.pdf"
                zf.writestr(nom_fichier, pro.carte_visite.read())

    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="commande-{str(order_id)[:8]}.zip"'
    return response

def _increment_downloads(order: Order):
    """
    Incrémente les téléchargements des contrats et packs de la commande.
    F() évite les race conditions si deux webhooks arrivent simultanément.
    """
    items = order.order_items.all()
    contrat_ids = [item.contrat_id for item in items if item.contrat_id is not None]
    pack_ids = [item.pack_id for item in items if item.pack_id is not None]

    if contrat_ids:
        Contrat.objects.filter(id__in=contrat_ids).update(
            downloads=F('downloads') + 1
        )
    if pack_ids:
        Pack.objects.filter(id__in=pack_ids).update(
            downloads=F('downloads') + 1
        )

def _send_download_email(order: Order):
    """
    Envoie le lien de téléchargement après paiement confirmé.
    - User connecté → lien simple (il s'auth lui-même)
    - Invité        → lien avec ?email= (order.guest.email via order.buyer_email)
    """
    buyer_email   = order.buyer_email
    base_url      = settings.FRONTEND_URL.rstrip('/')
    download_path = f'/payment/download/{order.id}/'

    if order.guest:
        download_url = f'{base_url}{download_path}?email={buyer_email}'
    else:
        download_url = f'{base_url}{download_path}'

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