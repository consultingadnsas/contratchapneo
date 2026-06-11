import logging
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404

from .models import Transaction
from .serializers import (
    TransactionSerializer,
    PaymentInitiateSerializer,
    PaymentSimulateSerializer,
)
from ecommerce.models import Order, Cart  # adapte le chemin

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentInitiateView(APIView):
    """
    POST /payments/initiate/
    Crée une Transaction PENDING liée à une commande.
    Retourne un payment_url simulé que le frontend peut "suivre".
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_id       = serializer.validated_data['order_id']
        payment_method = serializer.validated_data.get('payment_method', 'STRIPE')

        # Récupération de la commande
        order = get_object_or_404(Order, id=order_id)

        # Vérification d'accès (j'utilise ta méthode _can_access)
        if hasattr(self, '_can_access') and not self._can_access(request, order):
            return Response({'error': 'Accès interdit'}, status=status.HTTP_403_FORBIDDEN)

        try:
            with db_transaction.atomic():
                # 2. Stripe veut un montant en CENTIMES. 
                # Adapte `order.total_price` selon le nom de ton champ sur le modèle Order
                montant_en_centimes = int(order.total_amount * 100) 

                # 3. Création du PaymentIntent chez Stripe
                intent = stripe.PaymentIntent.create(
                    amount=montant_en_centimes,
                    currency='xof', # ⚠️ Remplace par ta devise ('xof', 'usd'...)
                    metadata={
                        'order_id': order.id,
                        # Sécurité supplémentaire pour les logs Stripe
                        'is_guest': order.guest is not None, 
                    }
                )

                # 4. Création de ta Transaction en base de données
                txn = Transaction.objects.create(
                    order=order,
                    amount=order.total_amount,
                    payment_method=payment_method,
                    status=Transaction.TransactionStatus.PENDING,
                    # 💡 ASTUCE CLÉ : On sauvegarde l'ID du PaymentIntent Stripe (pi_xxxx) 
                    # dans le provider_reference. Ce sera vital pour ton Webhook plus tard !
                    provider_reference=intent.id 
                )

                # 5. On renvoie le client_secret au Frontend (Nuxt 3)
                return Response({
                    'message': 'Intention de paiement Stripe créée avec succès',
                    'transaction_id': txn.id,
                    'client_secret': intent.client_secret,
                }, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            logger.error(f"Erreur Stripe : {str(e)}")
            return Response(
                {'error': "Erreur lors de la communication avec le service de paiement."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Erreur interne lors de l'initiation du paiement : {str(e)}")
            return Response(
                {'error': 'Une erreur est survenue.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _can_access(self, request, order):
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return order.guest is not None and order.guest.email == email

    def _build_payment_url(self, txn):
        """
        En simulation, on renvoie juste une URL interne vers la vue de simulation.
        En prod, ce serait l'URL de redirection CinetPay / Wave / etc.
        """
        return f"/payments/simulate/?transaction_id={txn.id}"


class PaymentSimulateView(APIView):
    """
        POST /payments/simulate/
        Simule un succès ou un échec de paiement.
        À remplacer par le vrai webhook prestataire en production.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PaymentSimulateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        transaction_id = serializer.validated_data['transaction_id']
        outcome        = serializer.validated_data['outcome']

        try:
            with db_transaction.atomic():
                txn = Transaction.objects.select_for_update().get(id=transaction_id)

                # Idempotence — on ne retraite pas une transaction déjà finalisée
                if txn.status != Transaction.TransactionStatus.PENDING:
                    return Response(
                        {
                            'data'   : TransactionSerializer(txn).data,
                            'message': 'Transaction déjà traitée.',
                        },
                        status=status.HTTP_200_OK
                    )

                if outcome == 'SUCCESS':
                    txn.status             = Transaction.TransactionStatus.SUCCESSFUL
                    txn.provider_reference = f"SIM-{txn.id}"  # référence simulée
                    txn.save()

                    order        = txn.order
                    order.status = Order.Status.PAID
                    order.save()

                    # Vider le panier maintenant que le paiement est confirmé
                    self._clear_cart(order)

                    logger.info(f"[SIMULATION] Paiement validé — commande {order.id}")

                    return Response(
                        {
                            'data'   : TransactionSerializer(txn).data,
                            'message': 'Paiement simulé avec succès. Commande confirmée.',
                        },
                        status=status.HTTP_200_OK
                    )

                else:  # FAILED
                    txn.status        = Transaction.TransactionStatus.FAILED
                    txn.error_message = "Paiement refusé (simulation)."
                    txn.save()

                    logger.warning(f"[SIMULATION] Paiement échoué — commande {txn.order.id}")

                    return Response(
                        {
                            'data'   : TransactionSerializer(txn).data,
                            'message': 'Paiement simulé échoué. La commande reste en attente.',
                        },
                        status=status.HTTP_200_OK
                    )

        except Transaction.DoesNotExist:
            return Response(
                {'message': 'Transaction introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def _clear_cart(self, order):
        """Vide le panier lié à la commande après confirmation du paiement."""
        try:
            if order.user:
                cart = order.user.cart
            else:
                # Invité : le panier est déjà vide après checkout,
                # mais on tente quand même par sécurité
                return
            cart.clear()
        except Exception:
            # Le panier peut ne plus exister — ce n'est pas bloquant
            pass


class PaymentWebhookView(APIView):
    """
    POST /payments/webhook/
    Webhook réel — à activer quand tu branches un vrai prestataire.
    Laissé en place mais non utilisé en simulation.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload            = request.data
        provider_reference = payload.get('transaction_id')
        payment_status     = payload.get('status')

        if not provider_reference:
            return Response({'error': 'Référence manquante'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                txn = Transaction.objects.select_for_update().get(
                    provider_reference=provider_reference
                )

                if txn.status != Transaction.TransactionStatus.PENDING:
                    return Response({'message': 'Déjà traité'}, status=status.HTTP_200_OK)

                if payment_status == 'SUCCESS':
                    txn.status             = Transaction.TransactionStatus.SUCCESSFUL
                    txn.save()
                    order        = txn.order
                    order.status = Order.Status.PAID
                    order.save()
                    logger.info(f"Paiement validé — commande {order.id}")

                elif payment_status == 'FAILED':
                    txn.status        = Transaction.TransactionStatus.FAILED
                    txn.error_message = payload.get('error_message', 'Raison non fournie')
                    txn.save()
                    logger.warning(f"Paiement échoué — commande {txn.order.id}")

            return Response({'message': 'Webhook traité'}, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            logger.error(f"Transaction inconnue — ref: {provider_reference}")
            return Response({'error': 'Transaction introuvable'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Erreur webhook : {str(e)}")
            return Response({'error': 'Erreur interne'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)