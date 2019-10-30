from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .serializers import *
from .models import *


class TipoCanchaViewSet(viewsets.ModelViewSet):
    queryset = TipoCancha.objects.all()
    serializer_class = TipoCanchaSerializer
    authentication_classes = (TokenAuthentication,)


class CanchaViewSet(viewsets.ModelViewSet):
    queryset = Cancha.objects.all()
    serializer_class = CanchaSerializer
    authentication_classes = (TokenAuthentication,)


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(empleado=self.request.user)

