from django.db.models import F
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.timezone import now
from .models import DailyVisit

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        """Extrait la véritable adresse IP (utile si tu as un reverse proxy comme Nginx)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        # 1. S'assurer que le visiteur a une clé de session[cite: 1]
        if not request.session.session_key:
            request.session.create()

        # 2. Marquer la visite pour ne pas recompter à chaque rechargement de page[cite: 1]
        if not request.session.get('has_visited_today'):
            request.session['has_visited_today'] = True
            
            ip = self.get_client_ip(request)
            country = 'Inconnu'
            
            # 3. Traduction de l'IP en pays (On ignore le localhost en dev)
            if ip and ip not in ['127.0.0.1', 'localhost']:
                try:
                    g = GeoIP2()
                    country = g.country_name(ip)
                except Exception:
                    pass # Base introuvable ou IP non répertoriée
            
            # 4. Incrémentation atomique (F()) pour gérer la concurrence[cite: 1]
            visit, created = DailyVisit.objects.get_or_create(date=now().date(), country=country)
            if not created:
                visit.visits = F('visits') + 1
                visit.save(update_fields=['visits'])

        return self.get_response(request)