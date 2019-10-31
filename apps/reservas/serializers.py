from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, CharField

from .models import *

class TipoCanchaSerializer(ModelSerializer):

    class Meta:
        model = TipoCancha
        fields = [
            'id',
            'tipo_cancha'
        ]


class CanchaSerializer(ModelSerializer):
    tipo = TipoCanchaSerializer()

    class Meta:
        model = Cancha
        fields = '__all__'


class ReservaSerializer(ModelSerializer):

    class Meta:
        model = Reserva
        fields = [
            'id',
            'cliente',
            'fecha_reserva',
            'cancha',
            'fecha_turno',
            'empleado'
        ]


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
