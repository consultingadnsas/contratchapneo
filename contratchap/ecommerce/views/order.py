import tempfile
import zipfile
import io
import os
from PIL.DdsImagePlugin import item
from PIL.Image import item
from django.http import FileResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F

from ..models import CartItem, Order, OrderItem, GuestInfo, Coupon
from ..serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    AddToCartSerializer,
    CheckoutSerializer,
)
from ..helpers import (get_or_create_cart, set_cart_cookie_if_needed)
from contrat.models import Contrat, CustomedContract, Pack, ContractRevision
from pro.models import LegalProfessional

from contrat.utils import fill_docx_template, convert_docx_to_pdf, send_documents_by_email_async

# ─────────────────────────────────────────
# ORDER VIEWS
# ─────────────────────────────────────────

class OrderListView(APIView):
    """
    GET /orders/
    Liste les commandes de l'utilisateur connecté.
    Non accessible aux invités (ils n'ont pas de compte).
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def get(self, request):
        orders = Order.objects.filter(
            user=request.user
        ).prefetch_related('order_items')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    """
        GET /orders/<order_id>/
        Détail d'une commande.
        Accessible au user connecté propriétaire OU à l'invité via son email.
    """
    permission_classes = [AllowAny]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.prefetch_related('order_items'),
            id=order_id
        )

        # Vérification d'accès
        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé à cette commande.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id):
        order = get_object_or_404(
            Order.objects.prefetch_related('order_items'),
            id=order_id
        )

        # Vérification d'accès
        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé à cette commande.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # 1. Mise à jour de la commande principale (Order)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        # 2. 🔥 LA CORRECTION EST ICI 🔥
        # On récupère directement le dictionnaire 'user_inputs' envoyé par ton frontend
        user_inputs_data = request.data.get('user_inputs') 
        
        if user_inputs_data:
            # Comme le frontend n'envoie pas l'ID de l'item, on prend le premier item de la commande
            item = order.order_items.first()
            
            if item:
                # /!\ Vérifie le nom exact de ton champ dans models.py !
                # Si ton champ s'appelle "user_item", utilise item.user_item = user_inputs_data
                item.user_inputs = user_inputs_data  
                
                # On sauvegarde uniquement ce champ pour l'item
                item.save(update_fields=['user_inputs']) 
                print("✅ Succès : user_inputs enregistrés sur l'item !")

        # 3. On renvoie la donnée fraîche
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    def _can_access(self, request, order):
        """
        User connecté → doit être le propriétaire.
        Invité        → doit fournir son email en query param.
        """
        if request.user.is_authenticated:
            return order.user == request.user

        # Invité : GET /orders/<id>/?email=john@example.com
        email = request.query_params.get('email', '').lower().strip()
        return (
            order.guest is not None and
            order.guest.email == email
        )
    
class OrderDownloadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, order_id):
        # 1. Récupération de la commande
        order = get_object_or_404(
            Order.objects.prefetch_related('order_items__contrat', 'order_items__pro'), 
            id=order_id
        )

        # 2. Vérification des accès
        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé à ce téléchargement.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if order.download_count >= 3:
            raise PermissionDenied("Limite atteinte : Vous avez déjà téléchargé ces documents 3 fois. Veuillez contacter le support si besoin.")

        # 🎯 L'ASTUCE EST ICI : On vérifie si c'est le tout premier essai (compteur à 0)
        is_first_download = (order.download_count == 0)

        # On incrémente le compteur pour la base de données
        order.download_count = F('download_count') + 1
        order.save(update_fields=['download_count'])

        # 3. Génération ou récupération des fichiers
        with tempfile.TemporaryDirectory() as temp_dir:
            generated_files = [] 

            for item in order.order_items.all():
                # --- CAS A : Contrat ---
                if item.contrat:
                    contrat = item.contrat
                    user_inputs = item.user_inputs or {} 
                    
                    if not contrat.fichier_modele or not contrat.fichier_modele.path:
                        continue  
                        
                    filled_docx_path = os.path.join(temp_dir, f"temp_{item.id}.docx")
                    fill_docx_template(contrat.fichier_modele.path, user_inputs, filled_docx_path)
                    
                    pdf_filename = f"{contrat.title.replace(' ', '_')}_{order.id}.pdf"
                    pdf_path = os.path.join(temp_dir, pdf_filename)
                    
                    convert_docx_to_pdf(filled_docx_path, temp_dir)
                    generated_temp_pdf = os.path.join(temp_dir, f"temp_{item.id}.pdf")
                    
                    if os.path.exists(generated_temp_pdf):
                        os.rename(generated_temp_pdf, pdf_path)
                        generated_files.append((pdf_filename, pdf_path))

                # --- CAS B : Professionnel ---
                elif item.pro:
                    if item.pro.visiting_card and hasattr(item.pro.visiting_card, 'path'):
                        pdf_path = item.pro.visiting_card.path
                        
                        if os.path.exists(pdf_path):
                            prenom = getattr(item.pro, 'first_name', 'Pro')
                            nom = getattr(item.pro, 'last_name', '')
                            pdf_filename = f"Carte_Visite_{prenom}_{nom}.pdf".replace(" ", "_")
                            generated_files.append((pdf_filename, pdf_path))

            if not generated_files:
                return Response(
                    {'message': 'Aucun document trouvé pour cette commande.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # 🚀 4. ENVOI EMAIL CONDITIONNEL
            # On n'exécute ce bloc lourd en RAM que si c'est le premier téléchargement
            if is_first_download:
                email_attachments = []
                for filename, path in generated_files:
                    with open(path, 'rb') as f:
                        email_attachments.append({
                            'filename': filename,
                            'content': f.read(),
                            'mimetype': 'application/pdf'
                        })
                
                to_email = order.guest.email if order.guest else request.user.email
                sujet = f"Vos documents juridiques Contratchap - Commande {str(order.id)[:8]}"
                message_body = f"""Bonjour,

                    Merci pour votre confiance !
                    Vous trouverez en pièce jointe les documents de votre commande.

                    L'équipe Contratchap."""

                send_documents_by_email_async(
                    subject=sujet, 
                    message=message_body, 
                    to_email=to_email, 
                    attachments_data=email_attachments
                )

            # 5. Renvoyer le fichier au navigateur (exécuté à chaque fois, jusqu'à 3)
            if len(generated_files) == 1:
                filename, path = generated_files[0]
                with open(path, 'rb') as f:
                    pdf_bytes = f.read()
                
                buffer = io.BytesIO(pdf_bytes)
                buffer.seek(0)
                
                response = FileResponse(buffer, as_attachment=True, filename=filename)
                response['Content-Type'] = 'application/pdf'
            else:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for filename, path in generated_files:
                        zip_file.write(path, arcname=filename)
                
                zip_buffer.seek(0)
                zip_filename = f"Documents_Contratchap_{order.id}.zip"
                
                response = FileResponse(zip_buffer, as_attachment=True, filename=zip_filename)
                response['Content-Type'] = 'application/zip'

            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response

    def _can_access(self, request, order):
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return (
            order.guest is not None and
            order.guest.email == email
        )


class OrderCancelView(APIView):
    """
    POST /orders/<order_id>/cancel/
    Annule une commande en statut 'pending'.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if not self._can_access(request, order):
            return Response(
                {'message': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not order.can_be_cancelled():
            return Response(
                {'message': f'Une commande avec le statut « {order.get_status_display()} » ne peut pas être annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = Order.Status.CANCELLED
        order.save()

        return Response(
            {
                'data'   : OrderSerializer(order).data,
                'message': 'Commande annulée avec succès.'
            },
            status=status.HTTP_200_OK
        )

    def _can_access(self, request, order):
        if request.user.is_authenticated:
            return order.user == request.user
        email = request.query_params.get('email', '').lower().strip()
        return (
            order.guest is not None and
            order.guest.email == email
        )