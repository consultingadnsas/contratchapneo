from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .models import Consulting
from .serializers import ConsultingSerializer


class ConsultingView(APIView):
    """
    Prise de rendez-vous pour le diagnostic juridique.
    Accessible publiquement depuis le tunnel client.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConsultingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                consulting = serializer.save()
            except IntegrityError:
                return Response(
                    {"detail": "Ce créneau vient d'être réservé par un autre utilisateur."},
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookedSlotsView(APIView):
    """
    Renvoie la liste des créneaux horaires déjà réservés pour une date donnée (date=YYYY-MM-DD).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'booked_slots': []}, status=status.HTTP_200_OK)

        booked = Consulting.objects.filter(meet_day=date_str).values_list('consulting_hour', flat=True)
        # Formater au format 'HH:MM' (ex: "09:30") et "09h30" pour faciliter le matching côté front
        slots = []
        for h in booked:
            formatted_colon = h.strftime('%H:%M')
            formatted_h = h.strftime('%Hh%M')
            slots.extend([formatted_colon, formatted_h])
            
        return Response({'booked_slots': list(set(slots))}, status=status.HTTP_200_OK)


class AdminConsultingListView(APIView):
    """
    Lister tous les rendez-vous pris pour l'espace d'administration (AdminInbox).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        consultings = Consulting.objects.all().order_by('-created_at')
        serializer = ConsultingSerializer(consultings, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class AdminConsultingDetailView(APIView):
    """
    Gérer un rendez-vous spécifique (voir, marquer comme traité / modifier le statut, supprimer).
    """
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        consulting = get_object_or_404(Consulting, pk=pk)
        serializer = ConsultingSerializer(consulting)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        consulting = get_object_or_404(Consulting, pk=pk)
        serializer = ConsultingSerializer(consulting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        consulting = get_object_or_404(Consulting, pk=pk)
        consulting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)