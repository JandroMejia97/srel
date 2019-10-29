from django.shortcuts import render

from rest_framework import viewsets, permissions

from .serializers import *
from .models import *


class TipoCanchaViewSet(viewsets.ModelViewSet):
    queryset = TipoCancha.objects.all()
    serializer_class = TipoCanchaSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CanchaViewSet(viewsets.ModelViewSet):
    queryset = Cancha.objects.all()
    serializer_class = CanchaSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(empleado=self.request.user)

