from django.urls import path
from .views import (
    ConsultingView, 
    BookedSlotsView, 
    AdminConsultingListView, 
    AdminConsultingDetailView
)

urlpatterns = [
    # Prise de RDV public
    path("consultings/", ConsultingView.as_view(), name="consulting-create"),
    # Consultation des créneaux réservés
    path("booked-slots/", BookedSlotsView.as_view(), name="consulting-booked-slots"),
    # Espace d'administration
    path("admin/consultings/", AdminConsultingListView.as_view(), name="admin-consulting-list"),
    path("admin/consultings/<uuid:pk>/", AdminConsultingDetailView.as_view(), name="admin-consulting-detail"),
]