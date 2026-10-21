from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError

from .models import Consulting
from .serializers import ConsultingSerializer


class ConsultingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConsultingSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                # Cas rare : deux requêtes simultanées sur le même créneau
                return Response(
                    {"detail": "Ce créneau vient d'être réservé."},
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)