import secrets
import string
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string

def generate_password_reset_token(user):
    """Génère un token sécurisé à 6 caractères et le sauvegarde en base"""
    # Alphabet sans caractères ambigus (optionnel mais recommandé pour les codes)
    alphabet = string.ascii_uppercase + string.digits
    short_token = ''.join(secrets.choice(alphabet) for _ in range(6))
    
    expires_at = timezone.now() + timedelta(hours=1)
    
    # Import ici pour éviter les dépendances circulaires
    from .models import PasswordResetToken
    
    # Supprime les anciens tokens et crée le nouveau
    PasswordResetToken.objects.filter(user=user).delete()
    PasswordResetToken.objects.create(
        user=user,
        token=short_token,
        expires_at=expires_at
    )
    return short_token

def send_welcome_email(user):
    """Envoie un email de bienvenue après l'inscription"""
    subject = "Bienvenue sur notre plateforme !"
    
    context = {
        'user': user,
        'frontend_url': settings.FRONTEND_URL,
    }
    
    html_content = render_to_string('account/welcome.html', context)
    
    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.content_subtype = "html"
    email.send()

def send_password_reset_email(user, reset_link):
    """Envoie un email avec token visible ET bouton cliquable"""
    subject = "Réinitialisation de votre mot de passe"
    
    context = {
        'user': user,
        'reset_link': reset_link,
        # La magie opère ici : split va automatiquement récupérer ton code à 6 caractères
        'token': reset_link.split('/')[-1],
        'frontend_url': settings.FRONTEND_URL,
    }
    
    html_content = render_to_string('account/password_reset.html', context)
    
    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.content_subtype = "html"
    email.send()

def send_password_change_confirmation(user):
    # Reste inchangé...
    subject = "Confirmation de changement de mot de passe"
    
    context = {
        'user': user,
        'frontend_url': settings.FRONTEND_URL,
    }
    
    html_content = render_to_string('account/password_changed.html', context)
    
    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.content_subtype = "html"
    email.send()