from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField

from .models import *

class TipoCanchaSerializer(ModelSerializer):

    class Meta:
        model = TipoCancha
        fields = [
            'id',
            'tipo_cancha'
        ]


class CanchaReadSerializer(ModelSerializer):
    tipo = TipoCanchaSerializer()

    class Meta:
        model = Cancha
        fields = [
            'id',
            'tipo',
            'nombre',
            'cod_interno',
            'tiene_vestuario',
            'tiene_iluminacion',
            'tiene_cesped_sintetico',
        ]


class CanchaSerializer(ModelSerializer):
    tipo = PrimaryKeyRelatedField(queryset=TipoCancha.objects.all())

    class Meta:
        model = Cancha
        fields = [
            'id',
            'tipo',
            'nombre',
            'cod_interno',
            'tiene_vestuario',
            'tiene_iluminacion',
            'tiene_cesped_sintetico',
        ]


class ReservaSerializer(ModelSerializer):

    class Meta:
        model = Reserva
        fields = [
            'id',
            'cliente',
            'fecha_reserva',
            'cancha',
            'fecha_turno',
            'hora_turno',
            'empleado'
        ]
        depth = 1


class UserSerializer(ModelSerializer):
    password = CharField()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password'
        ]
