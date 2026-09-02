from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.db.models import Q, Sum, F
from django.utils.timezone import now
from django.contrib.gis.geoip2 import GeoIP2

from .models import DailyVisit
from .serializers import DailyVisitSerializer
# Importe ta classe de pagination (ajuste le chemin si besoin)
from payments.views import AdminCartPagination

class AdminDailyVisitView(ListAPIView):
    """
    GET /admin/visitors/?page=1&country=France&start_date=2026-09-01
    Retourne la liste paginée et filtrée des visites journalières.
    Accessible uniquement aux administrateurs.
    """
    permission_classes = [IsAdminUser] #[cite: 9]
    serializer_class = DailyVisitSerializer
    pagination_class = AdminCartPagination #[cite: 9]

    def get_queryset(self):
        # Par défaut, on trie de la date la plus récente à la plus ancienne
        queryset = DailyVisit.objects.all().order_by('-date', '-visits')

        # 1. Filtre par pays (recherche partielle, insensible à la casse)
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)

        # 2. Filtre par date de début
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        # 3. Filtre par date de fin
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset


class VisitAPIView(APIView):
    """
    Endpoint public pour enregistrer une visite (POST) et obtenir les stats du jour (GET).
    - POST: enregistre une visite unique par session et par jour.
    - GET: retourne le total des visites du jour par pays et en global.
    """
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def post(self, request, *args, **kwargs):
        # Utiliser une clé qui inclut la date pour réinitialiser quotidiennement
        key = f"has_visited_{now().date()}"
        if not request.session.session_key:
            request.session.create()

        if not request.session.get(key):
            request.session[key] = True

            ip = self.get_client_ip(request)
            country = 'Inconnu'
            if ip and ip not in ['127.0.0.1', 'localhost']:
                try:
                    g = GeoIP2()
                    country = g.country_name(ip) or country
                except Exception:
                    pass

            visit, created = DailyVisit.objects.get_or_create(date=now().date(), country=country)
            if created:
                # créé avec visits=0 par défaut, on incrémente explicitement
                visit.visits = F('visits') + 1
                visit.save(update_fields=['visits'])
            else:
                visit.visits = F('visits') + 1
                visit.save(update_fields=['visits'])

        # Assurer que le cookie CSRF est présent pour les appels ultérieurs
        csrf_token = get_token(request)

        # Retourner les stats du jour
        today = now().date()
        qs = DailyVisit.objects.filter(date=today).values('country').annotate(visits=Sum('visits'))
        total = sum([item['visits'] for item in qs]) if qs else 0
        resp = Response({'date': str(today), 'total_visits': total, 'by_country': list(qs)})
        # Placer le cookie CSRF pour que les clients JS puissent le lire
        resp.set_cookie('csrftoken', csrf_token, httponly=False, samesite='Lax', path='/')
        resp['X-CSRFToken'] = csrf_token
        return resp

    def get(self, request, *args, **kwargs):
        today = now().date()
        qs = DailyVisit.objects.filter(date=today).values('country').annotate(visits=Sum('visits'))
        total = sum([item['visits'] for item in qs]) if qs else 0
        resp = Response({'date': str(today), 'total_visits': total, 'by_country': list(qs)})
        csrf_token = get_token(request)
        resp.set_cookie('csrftoken', csrf_token, httponly=False, samesite='Lax', path='/')
        resp['X-CSRFToken'] = csrf_token
        return resp