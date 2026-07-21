from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.middleware.csrf import get_token

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

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(
            {'user': serializer.data},
            status=status.HTTP_200_OK
        )

# ===========================================
# Relation about Contract
# ===========================================

class UserPackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        packs = UserPack.objects.filter(user=request.user)
        serializer = PackSerializer(packs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
