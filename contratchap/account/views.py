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
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Vérification des champs obligatoires
        if not password:
            return Response(
                {'error': 'Veuillez fournir un mot de passe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email and not username:
            return Response(
                {'error': 'Veuillez fournir un email ou un nom d\'utilisateur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentification par email
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                username = user.username  # On récupère le username pour l'authentification
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Email ou mot de passe incorrect.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            # Authentification par username
            username = username

        # CORRECTION: authenticate() ne prend pas 'email' comme paramètre
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {'error': 'Votre compte est désactivé.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Création de la reponse
            response = Response({
               'user': {
                   'user':user.id,
                    'username': user.username,
                    'email':user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message':'Connexion Réussie.'
            }, status=status.HTTP_200_OK
            )

            # Définir les cookies HttpOnly
            # Access Token cookie (15 minutes ou 1 jour selon votre configuration)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                max_age=24 * 60 * 60,  # 1 jour (votre settings)
            )

            # Refresh Token cookie (7 jours)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                max_age=7 * 24 * 60 * 60,  # 7 jours
            )

            return response
        
        else:
            return Response(
                {'error': 'Email/Nom d\'utilisateur ou mot de passe incorrect.'},
                status=status.HTTP_401_UNAUTHORIZED
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

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(
            {'user': serializer.data},
            status=status.HTTP_200_OK
        )