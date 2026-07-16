# payment/views.py
import json
import requests  # pip install requests
import zipfile
import io
import tempfile
import os

from django.http    import FileResponse
from django.conf    import settings
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import AllowAny

from ecommerce.models import Order
from contrat.models   import Contrat
from .models          import Transaction
from .serializers     import (
    TransactionSerializer,
    PaymentInitiateSerializer,
    PaymentSimulateSerializer,
)

from .utils import (
    stream_single_pdf, 
    stream_zip, 
    _increment_downloads, 
    _send_download_email
)

from contrat.utils import fill_docx_template, convert_docx_to_pdf

# ─────────────────────────────────────────
# INITIATE  —  POST /payment/initiate/
# ─────────────────────────────────────────

class PaymentInitiateView(APIView):
    """
    POST /payment/initiate/
    Crée une Transaction PENDING, appelle l'API sandbox xpaye,
    et retourne l'URL de redirection vers leur page de paiement.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_id       = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']

        # On précharge guest et user pour éviter des requêtes supplémentaires
        order = get_object_or_404(
            Order.objects.select_related('guest', 'user'),
            id=order_id
        )

        if order.status != Order.Status.PENDING:
            return Response(
                {'message': f'Commande non payable (statut : {order.get_status_display()}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Créer la Transaction — son UUID devient notre referenceNumber ──
        transaction = Transaction.objects.create(
            order              = order,
            amount             = order.total_amount,
            payment_method     = payment_method,
            status             = Transaction.TransactionStatus.PENDING,
            provider_reference = None,
        )
        transaction.provider_reference = str(transaction.id)
        transaction.save(update_fields=['provider_reference'])

        # ── Décomposer le nom (GuestInfo.full_name → first / last) ────────
        if order.guest:
            # GuestInfo.full_name = "Ishola Lamine" → split sur le premier espace
            name_parts = order.guest.full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            last_name  = name_parts[1] if len(name_parts) > 1 else ''
            phone      = order.guest.phone_number   # GuestInfo.phone_number
        else:
            first_name = getattr(order.user, 'first_name', '') or ''
            last_name  = getattr(order.user, 'last_name',  '') or ''
            phone      = getattr(order.user, 'phone_number', '') or ''

        # ── Payload calé sur leur format sandbox ──────────────────────────
        xpaye_payload = {
            'merchantId'         : settings.XPAYE_MERCHANT_ID,
            'amount'             : int(order.total_amount),      # entier FCFA
            'description'        : f'Commande {str(order.id)[:8]}',
            'channel'            : 'CARD',
            'countryCurrencyCode': '952',                        # FCFA XOF
            'referenceNumber'    : str(transaction.id),          # ← notre clé de récup
            'customerEmail'      : order.buyer_email,            # property Order
            'customerFirstName'  : first_name,
            'customerLastname'   : last_name,
            'customerPhoneNumber': phone,
            'notificationURL'    : settings.XPAYE_NOTIFICATION_URL,
            'returnURL'          : settings.XPAYE_RETURN_URL,
            'returnContext'      : json.dumps({'order_id': str(order.id)}),
        }

        # ── Appel API sandbox xpaye ───────────────────────────────────────
        try:
            xpaye_resp = requests.post(
                settings.XPAYE_API_URL,
                json    = xpaye_payload,
                timeout = 15,
            )
            # 💡 ASTUCE DEBUG : Affiche la réponse brute de la sandbox dans ton terminal Django
            print(f"--- STATUS XPAYE : {xpaye_resp.status_code} ---")
            print(f"--- REPONSE XPAYE : {xpaye_resp.text} ---")
            xpaye_resp.raise_for_status()
            xpaye_data = xpaye_resp.json()
        except requests.RequestException as e:
            # Transaction reste PENDING → l'utilisateur peut réessayer
            return Response(
                {'message': 'Erreur de connexion à xpaye.', 'error': str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # ── Réponse xpaye : {"success": true, "message": "...", "url": "..."} ──
        if not xpaye_data.get('success'):
            # xpaye a répondu mais avec un échec applicatif
            transaction.status        = Transaction.TransactionStatus.FAILED
            transaction.error_message = xpaye_data.get('message', 'Échec retourné par xpaye.')
            transaction.save(update_fields=['status', 'error_message'])

            return Response(
                {'message': xpaye_data.get('message', 'Paiement non initialisé.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Succès → retourner l'URL au frontend pour redirection ─────────
        return Response(
            {
                'data'       : TransactionSerializer(transaction).data,
                'payment_url': xpaye_data.get('url'),   # "https://sandbox.paiementpro.net/..."
                'message'    : xpaye_data.get('message', 'Initialisation réussie.'),
            },
            status=status.HTTP_201_CREATED
        )

# ─────────────────────────────────────────
# SIMULATE  —  POST /payment/simulate/
# (sandbox / DEBUG uniquement)
# ─────────────────────────────────────────

class PaymentSimulateView(APIView):
    """
    Simule un retour xpaye sans appeler leur API.
    Désactivé automatiquement hors DEBUG.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if not settings.DEBUG:
            return Response(
                {'message': 'Endpoint non disponible en production.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PaymentSimulateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction_id = serializer.validated_data['transaction_id']
        outcome        = serializer.validated_data['outcome']   # 'SUCCESS' ou 'FAILED'

        transaction = get_object_or_404(
            Transaction.objects.select_related('order__guest', 'order__user'),
            id=transaction_id
        )

        if transaction.status != Transaction.TransactionStatus.PENDING:
            return Response(
                {'message': f'Transaction déjà traitée ({transaction.get_status_display()}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if outcome == 'SUCCESS':
            transaction.status = Transaction.TransactionStatus.SUCCESSFUL
            transaction.save()

            order        = transaction.order
            order.status = Order.Status.PAID
            order.save()

            _increment_downloads(order)
            _send_download_email(order)

        else:
            transaction.status        = Transaction.TransactionStatus.FAILED
            transaction.error_message = 'Échec simulé manuellement (sandbox).'
            transaction.save()

        return Response(
            {
                'data'   : TransactionSerializer(transaction).data,
                'message': f'Simulation terminée : {outcome}.',
            },
            status=status.HTTP_200_OK
        )


# ─────────────────────────────────────────
# WEBHOOK  —  POST /payment/webhook/
# ─────────────────────────────────────────

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def payment_webhook_view(request):
    """
    Reçoit la notification xpaye après paiement.
    Met à jour la transaction, la commande, et envoie l'email.
    On répond TOUJOURS 200 pour éviter les réessais intempestifs de xpaye.
    """
    try:
        data = request.data if request.data else json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'message': 'Payload JSON invalide.'}, status=status.HTTP_200_OK)

    #print("Webhook reçu :", data)

    reference      = data.get('referenceNumber')
    response_code  = data.get('responsecode')
    pay_status     = data.get('status')
    success_flag   = data.get('success')
    error_msg      = data.get('message', '')

    # XPAYE peut envoyer un code numérique (0 = succès) ou un statut texte.
    is_success = (
        str(response_code) == '0'
        or str(pay_status).upper() in {'SUCCESS', 'SUCCEEDED', 'PAID', 'OK'}
        or str(success_flag).upper() in {'TRUE', '1', 'SUCCESS', 'SUCCEEDED'}
    )

    if not reference:
        return Response({'message': 'referenceNumber manquant.'}, status=status.HTTP_200_OK)

    try:
        transaction = Transaction.objects.select_related(
            'order__guest', 'order__user'
        ).get(provider_reference=reference)
    except Transaction.DoesNotExist:
        return Response({'message': 'Transaction inconnue.'}, status=status.HTTP_200_OK)

    # Idempotence
    if transaction.status != Transaction.TransactionStatus.PENDING:
        return Response({'message': 'Déjà traité.'}, status=status.HTTP_200_OK)

    if is_success:
        transaction.status = Transaction.TransactionStatus.SUCCESSFUL
        transaction.error_message = None
        transaction.save(update_fields=['status', 'error_message'])

        order = transaction.order
        order.status = Order.Status.PAID
        order.save(update_fields=['status'])

        if order.user:  
            for item in order.order_items.all():
                # Si la ligne de commande contient un pack
                if item.pack: 
                    # On importe le modèle qui relie l'User au Pack (à mettre tout en haut de ton fichier views.py)
                    from contrat.models import UserPack 

                    # On livre le pack à l'utilisateur !
                    UserPack.objects.create(
                        user=order.user,
                        pack=item.pack,
                        # Attention: vérifie le nom exact de ton champ de crédits sur tes modèles UserPack et Pack
                        credits_restants=item.pack.nombre_credits 
                    )

        _increment_downloads(order)
        #_send_download_email(order)

        return Response(
            {'message': 'Paiement confirmé — téléchargement prêt.'},
            status=status.HTTP_200_OK
        )

    transaction.status = Transaction.TransactionStatus.FAILED
    transaction.error_message = error_msg or (
        f"Échec du paiement (responsecode={response_code})."
    )
    transaction.save(update_fields=['status', 'error_message'])

    return Response(
        {'message': 'Paiement échoué.'},
        status=status.HTTP_200_OK
    )

# ─────────────────────────────────────────
# Générer CONTRACT  —  GET /payment/download/<order_id>/
# ─────────────────────────────────────────

class GenerateContractView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, order_id):
        # On va précharger le pro et le user
        order = get_object_or_404(
            Order.objects.prefetch_related(
                'order_items__contrat'
            ).select_related('guest', 'user'),
            id=order_id
        )

        if not self._can_access(request, order):
            return Response({'message': 'Accès non autorisé'})
        
        if order.status != Order.Status.PAID:
            return Response(
                {'message': f'Commande non payée (statut : {order.get_status_display()})'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        contracts = []
        
    def _can_access(self, request, order) -> bool:
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return (order.guest is not None and order.guest.email == email)



# ─────────────────────────────────────────
# DOWNLOAD  —  GET /payment/download/<order_id>/
# ─────────────────────────────────────────

class DownloadContractView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.prefetch_related(
                'order_items__contrat',
                'order_items__pro__user'
            ).select_related('guest', 'user'),
            id=order_id
        )

        if not self._can_access(request, order):
            return Response({'message': 'Accès non autorisé.'}, status=status.HTTP_403_FORBIDDEN)

        if order.status != Order.Status.PAID:
            return Response({'message': 'Commande non payée.'}, status=status.HTTP_403_FORBIDDEN)

        # 1. On garde LES ITEMS entiers (pas juste les contrats) pour avoir accès à item.user_inputs !
        contract_items = [
            item for item in order.order_items.all()
            if getattr(item, 'contrat', None) and item.contrat.fichier_modele
        ]
        
        pro_items = [
            item for item in order.order_items.all()
            if getattr(item, 'pro_id', None) and getattr(item, 'pro', None) and item.pro.visiting_card 
        ]

        if not contract_items and not pro_items:
            return Response({'message': 'Aucun fichier disponible.'}, status=status.HTTP_404_NOT_FOUND)

        # 👇 Logique de téléchargement intelligente

        # Cas 1 : EXACTEMENT 1 contrat, AUCUN pro -> Génère et streame le contrat PDF
        if len(contract_items) == 1 and len(pro_items) == 0:
            return self._stream_single_contract(contract_items[0])
            
        # Cas 2 : AUCUN contrat, EXACTEMENT 1 pro -> Streame la carte de visite PDF
        if len(pro_items) == 1 and len(contract_items) == 0:
            pro = pro_items[0].pro
            nom_pro = f"Carte_visite_{pro.user.first_name}_{pro.user.last_name}.pdf" if pro.user else "Carte_visite.pdf"
            response = FileResponse(pro.visiting_card.open('rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nom_pro}"'
            return response

        # Cas 3 : Mixte (Plusieurs éléments) -> On ZIPPE tout ensemble
        return self._stream_zip(contract_items, pro_items, order_id)

    # -------------------------------------------------------------------------
    # 🛠️ FONCTIONS UTILITAIRES PRIVÉES (À rajouter dans la classe)
    # -------------------------------------------------------------------------

    def _generate_pdf_bytes(self, item):
        """Prend un OrderItem, génère le Word rempli, le convertit en PDF, et renvoie les octets"""
        template_path = item.contrat.fichier_modele.path
        user_inputs = item.user_inputs or {}  # Si vide, renvoie au moins un dictionnaire vide
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filled_docx_path = os.path.join(temp_dir, "temp_filled.docx")
            
            # 1. Remplissage
            fill_docx_template(template_path, user_inputs, filled_docx_path)
            # 2. Conversion
            pdf_path = convert_docx_to_pdf(filled_docx_path, temp_dir)
            
            # 3. Lecture en mémoire (pour que le fichier puisse être supprimé avec temp_dir)
            with open(pdf_path, 'rb') as f:
                return f.read()

    def _stream_single_contract(self, item):
        """Gère le téléchargement d'un unique contrat"""
        pdf_bytes = self._generate_pdf_bytes(item)
        
        # On utilise io.BytesIO pour streamer depuis la RAM au lieu du disque
        buffer = io.BytesIO(pdf_bytes)
        response = FileResponse(buffer, content_type='application/pdf')
        
        nom_fichier = f"Contrat_{item.contrat.title}.pdf" # Remplace 'titre' par 'title' si besoin
        response['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
        return response

    def _stream_zip(self, contract_items, pro_items, order_id):
        """Génère un fichier ZIP contenant les contrats dynamiques et les cartes pros"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # Ajout des contrats générés
            for index, item in enumerate(contract_items):
                pdf_bytes = self._generate_pdf_bytes(item)
                nom_fichier = f"Contrat_{item.contrat.titre}_{index+1}.pdf"
                zip_file.writestr(nom_fichier, pdf_bytes)
            
            # Ajout des cartes de visite
            for index, item in enumerate(pro_items):
                with item.pro.visiting_card.open('rb') as f:
                    nom_fichier = f"Carte_visite_{item.pro.user.first_name}_{index+1}.pdf" if item.pro.user else f"Carte_visite_{index+1}.pdf"
                    zip_file.writestr(nom_fichier, f.read())
                    
        zip_buffer.seek(0)
        response = FileResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="Commande_Contratchap_{order_id}.zip"'
        return response

    def _can_access(self, request, order) -> bool:
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return (order.guest is not None and order.guest.email == email)

# ─────────────────────────────────────────
# HELPERS PRIVÉS
# ─────────────────────────────────────────

def _increment_downloads(order: Order):
    """
    Incrémente Contrat.downloads pour chaque contrat de la commande.
    F() évite les race conditions si deux webhooks arrivent simultanément.
    """
    contrat_ids = [
        item.contrat_id
        for item in order.order_items.all()
        if item.contrat_id is not None
    ]
    if contrat_ids:
        Contrat.objects.filter(id__in=contrat_ids).update(
            downloads=F('downloads') + 1
        )




