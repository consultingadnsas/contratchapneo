import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction

from .models import Transaction
# from ecommerce.models import Order (selon comment ton app est structurée)

logger = logging.getLogger(__name__)

class PaymentWebhookView(APIView):
    """
    POST /payments/webhook/
    Écoute les notifications de paiement du prestataire externe.
    """
    # CRUCIAL : Le prestataire n'est pas un utilisateur connecté.
    # On doit autoriser n'importe qui à taper sur cette URL.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Récupération des données envoyées par la banque/prestataire
        payload = request.data

        # --- SÉCURITÉ (À adapter selon ton prestataire) ---
        # Normalement, Stripe ou CinetPay t'envoient un "Header" secret.
        # Il faut vérifier ce header pour s'assurer que c'est bien la banque
        # qui te parle, et pas un petit malin qui essaie de valider sa commande gratuitement.
        # if not self.verify_webhook_signature(request):
        #     return Response({'error': 'Signature invalide'}, status=403)
        # --------------------------------------------------

        try:
            # 2. Extraction des informations clés
            # ATTENTION : Les noms des clés ('transaction_id', 'status') dépendent 
            # de la documentation de ton prestataire spécifique.
            provider_reference = payload.get('transaction_id')
            payment_status = payload.get('status') # Ex: 'SUCCESS' ou 'FAILED'
            
            if not provider_reference:
                return Response({'error': 'Référence de transaction manquante'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Mise à jour de la base de données
            # On utilise une transaction atomique et un "select_for_update" 
            # pour éviter que deux webhooks simultanés ne corrompent la donnée.
            with transaction.atomic():
                txn = Transaction.objects.select_for_update().get(provider_reference=provider_reference)
                
                # Si le statut n'est plus PENDING, c'est qu'on a déjà traité ce webhook
                if txn.status != Transaction.TransactionStatus.PENDING:
                    return Response({'message': 'Transaction déjà traitée'}, status=status.HTTP_200_OK)

                if payment_status == 'SUCCESS':
                    # On valide la transaction
                    txn.status = Transaction.TransactionStatus.SUCCESSFUL
                    txn.save()

                    # On met à jour la commande principale
                    order = txn.order
                    order.status = 'PAID'  # Assure-toi d'utiliser la bonne constante de ton modèle Order
                    order.save()

                    # 🎯 C'est ICI que tu déclenches la logique métier post-achat :
                    # - Envoi de l'email avec le contrat PDF
                    # - Génération de la facture
                    logger.info(f"Paiement validé pour la commande {order.id}")

                elif payment_status == 'FAILED':
                    # On marque la transaction comme échouée
                    txn.status = Transaction.TransactionStatus.FAILED
                    txn.error_message = payload.get('error_message', 'Raison non fournie par la banque')
                    txn.save()
                    
                    logger.warning(f"Paiement échoué pour la commande {txn.order.id}")

            # Il faut TOUJOURS répondre 200 OK rapidement au prestataire, 
            # sinon il va croire que ton serveur est en panne et renvoyer le webhook en boucle.
            return Response({'message': 'Webhook reçu et traité'}, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            logger.error(f"Alerte : Transaction inconnue reçue - Ref: {provider_reference}")
            return Response({'error': 'Transaction introuvable'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Erreur fatale Webhook : {str(e)}")
            # On renvoie 500 pour que le prestataire réessaie plus tard si c'est un crash de notre DB
            return Response({'error': 'Erreur interne'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)