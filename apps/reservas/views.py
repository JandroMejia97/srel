from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import (
    viewsets,
    permissions,
    decorators,
    pagination,
    status
)
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *


class ShortResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class TipoCanchaViewSet(viewsets.ModelViewSet):
    queryset = TipoCancha.objects.all()
    serializer_class = TipoCanchaSerializer
    authentication_classes = (TokenAuthentication,)


class CanchaViewSet(viewsets.ModelViewSet):
    queryset = Cancha.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = ShortResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'tipo',
        'tiene_vestuario',
        'tiene_iluminacion',
        'tiene_cesped_sintetico'
    ]

    def get_serializer_class(self):
         if self.request.method in ['GET']:
             return CanchaReadSerializer
         return CanchaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    authentication_classes = (TokenAuthentication,)
    pagination_class = ShortResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'cancha',
        'fecha_reserva',
        'fecha_turno',
        'hora_turno',
        'cliente',
        'empleado'
    ]

    def perform_create(self, serializer):
        if self.request.user:
           serializer.save(empleado=self.request.user)
        elif 'Authorization' in self.request.headers:
            token_text = self.request.headers['Authorization'].split(' ')
            token = Token.objects.get(key=token_text[1])
            serializer.save(empleado=token.user)       

    def get_serializer_class(self):
         if self.request.method in ['GET']:
             return ReservaReadSerializer
         return ReservaSerializer


class OnlyPOST(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_destroy(self, serializer):
        if self.request.user.is_authenticated:
            serializer.delete(user=self.request.user)
        elif 'Authorization' in self.request.headers:
            token_text = self.request.headers['Authorization'].split(' ')
            token = Token.objects.get(key=token_text[1])
            serializer.delete(user=token.user)
