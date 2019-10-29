from rest_framework.serializers import ModelSerializer

from .models import *

class TipoCanchaSerializer(ModelSerializer):

    class Meta:
        model = TipoCancha
        fields = [
            'id',
            'tipo_cancha'
        ]


class CanchaSerializer(ModelSerializer):

    class Meta:
        model = Cancha
        fields = '__all__'


class ReservaSerializer(ModelSerializer):
    cancha = CanchaSerializer()

    class Meta:
        model = Reserva
        fields = [
            'id',
            'cliente',
            'fecha_reserva',
            'cancha',
            'fecha_turno'
        ]
