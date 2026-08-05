from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, PasswordResetToken
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q, F
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.middleware.csrf import get_token
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .utils import generate_password_reset_token, send_password_reset_email, send_welcome_email, send_password_change_confirmation
from django.conf import settings

# ===========================================
# Relation
# ===========================================

from contrat.models import (Pack, UserPack, Contrat, Category, CustomedContract)
from contrat.serializers import(ContratSerializer, PackSerializer)

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        
        # raise_exception=True intercepte automatiquement les erreurs et renvoie un 400 propre
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': _('Votre compte a été créé avec succès')
                }, status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'errors': serializer.errors,
                'message': _('Erreur lors de la création de compte')
            }, status=status.HTTP_400_BAD_REQUEST
        )
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # On accepte la clé 'username' ou 'email' pour une compatibilité maximale
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')

        if not password:
            return Response(
                {'error': 'Veuillez fournir un mot de passe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not identifier:
            return Response(
                {'error': 'Veuillez fournir un email ou un nom d\'utilisateur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Détection automatique : Recherche par email ou par nom d'utilisateur
        try:
            if '@' in identifier:
                user_obj = CustomUser.objects.get(email=identifier)
            else:
                user_obj = CustomUser.objects.get(username=identifier)
            
            # On extrait le username exact requis par authenticate()
            username = user_obj.username
        except CustomUser.DoesNotExist:
            # On retourne une erreur générique pour des raisons de sécurité
            return Response(
                {'error': 'Identifiants incorrects.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authentification officielle Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {'error': 'Votre compte est désactivé.'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
               'user': {
                   'user': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message': 'Connexion Réussie.'
            }, status=status.HTTP_200_OK
            )

            response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=24 * 60 * 60)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=7 * 24 * 60 * 60)

            return response
        
        else:
            return Response(
                {'error': 'Identifiants incorrects.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    # On permet l'accès à l'endpoint pour pouvoir vider les cookies même si l'access_token a expiré
    permission_classes = [AllowAny] 

    def post(self, request):
        # 1. Récupérer le refresh token depuis le cookie
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                # 2. Blacklister le token pour invalider la session côté serveur
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                # Si le token est déjà expiré ou invalide, on ignore l'erreur pour continuer le logout
                pass
        
        response = Response(
            {'message': 'Déconnexion réussie'},
            status=status.HTTP_200_OK
        )

        # 3. Supprimer les cookies côté client
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response        

class CSRFTokenView(APIView):
    """Initialise le token CSRF pour les requêtes cross-site"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        csrf_token = get_token(request)
        return Response(
            {'csrfToken': csrf_token},
            status=status.HTTP_200_OK
        )

class UserProfileView(APIView):
    """
    Vue permettant à un utilisateur connecté de consulter, 
    mettre à jour ou supprimer son profil.
    """
    permission_classes = [IsAuthenticated]

    # READ : Récupérer ses informations
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            {'user': serializer.data},
            status=status.HTTP_200_OK
        )

    # UPDATE (Complet) : Mettre à jour toutes les informations
    def put(self, request):
        # On passe l'instance de l'utilisateur actuel et les nouvelles données
        serializer = UserSerializer(request.user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'user': serializer.data,
                    'message': _('Profil mis à jour avec succès.')
                },
                status=status.HTTP_200_OK
            )
            
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # UPDATE (Partiel) : Mettre à jour seulement quelques champs (ex: juste le nom)
    def patch(self, request):
        # partial=True permet de ne pas exiger tous les champs obligatoires du modèle
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'user': serializer.data,
                    'message': _('Profil partiellement mis à jour.')
                },
                status=status.HTTP_200_OK
            )
            
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE : Supprimer son propre compte
    def delete(self, request):
        user = request.user
        user.delete() # Supprime l'utilisateur de la base de données
        
        return Response(
            {'message': _('Votre compte a été supprimé avec succès.')},
            status=status.HTTP_204_NO_CONTENT
        )

# ===========================================
# Relation about Contract
# ===========================================

class UserPackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        
        # 1️⃣ DÉSACTIVATION AUTOMATIQUE DES PACKS EXPIRÉS OU VIDES
        # On passe is_active=False en base de données si :
        # - La date d'expiration est dépassée
        # - OU (credits_restants == 0 ET customs_restants == 0 ET cartes_pro_restantes == 0)
        UserPack.objects.filter(
            user=request.user,
            is_active=True
        ).filter(
            Q(expires_at__lte=now) |
            Q(
                credits_restants__lte=0,
                customs_restants__lte=0,
                cartes_pro_restantes__lte=0
            )
        ).update(is_active=False)

        # 2️⃣ ON RÉCUPÈRE TOUS LES PACKS DE L'UTILISATEUR (Actifs et Expirés)
        # ⚡️ CORRECTION : On enlève "is_active=True" pour envoyer l'historique complet au front !
        packs = UserPack.objects.filter(
            user=request.user
        ).order_by('-id')  # Optionnel : met le pack le plus récent en premier
        
        serializer = PackSerializer(packs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response(
                {'error': 'Token et nouveau mot de passe requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()  # Vérifie que le token n'a pas expiré
            )
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Lien invalide ou expiré.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mettre à jour le mot de passe
        user = reset_token.user
        user.password = make_password(new_password)  # Hash le mot de passe
        user.save()

        # ENVOI DE L'EMAIL DE CONFIRMATION DE CHANGEMENT
        send_password_change_confirmation(user)

        # Supprimer le token utilisé (empêche la réutilisation)
        reset_token.delete()

        return Response(
            {'message': 'Mot de passe réinitialisé avec succès.'},
            status=status.HTTP_200_OK
        )

class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Veuillez fournir une adresse e-mail.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Pour des raisons de sécurité, on ne révèle pas si l'email existe
            return Response(
                {'message': 'Si un compte existe, un email a été envoyé.'},
                status=status.HTTP_200_OK
            )

        # Génération et envoi délégués aux utils
        token = generate_password_reset_token(user)
        reset_link = f'{settings.FRONTEND_URL}/reset-password/{token}'
        
        # ENVOI DE L'EMAIL DE RÉINITIALISATION (déjà présent)
        send_password_reset_email(user, reset_link)

        return Response(
            {'message': 'Si un compte existe, un email a été envoyé.'},
            status=status.HTTP_200_OK
        )

class PasswordResetTokenVerifyView(APIView):
    """
    Vérifie la validité d'un token de réinitialisation
    Exemple de requête : POST /api/password-reset/verify-token/
    {
        "token": "abc123..."
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response(
                {"valid": False, "message": "Token requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = PasswordResetToken.objects.get(
                token=token,
                expires_at__gt=timezone.now()  # Vérifie que le token n'a pas expiré
            )
            return Response({
                "valid": True,
                "message": "Token valide",
                "email": reset_token.user.email  # Optionnel : pour confirmation frontend
            })
            
        except PasswordResetToken.DoesNotExist:
            return Response({
                "valid": False,
                "message": "Token invalide ou expiré"
            }, status=status.HTTP_400_BAD_REQUEST)