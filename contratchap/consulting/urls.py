from django.urls import path
from .views import ConsultingView

urlpatterns = [
    path("consultings/", ConsultingView.as_view(), name="consulting"),
]