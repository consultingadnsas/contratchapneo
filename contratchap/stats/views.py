from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
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