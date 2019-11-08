from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import datetime


class TipoCancha(models.Model):
    tipo_cancha = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        help_text='Ingrese el tipo de cancha.' +
        'Ejemplo: Cancha 11, Cancha 7, etc.',
        verbose_name='Tipo de cancha',
    )

    def __str__(self):
        return self.tipo_cancha

    class Meta:
        verbose_name = 'Tipo de Cancha'
        verbose_name_plural = 'Tipos de Cancha'


class Cancha(models.Model):
    tipo = models.ForeignKey(
        to=TipoCancha,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Seleccione el tipo de cancha',
        verbose_name='Tipo de cancha',
    )
    nombre = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text='Ingrese el nombre de la cancha. ' +
        'Ejemplo: La Diego Armando',
        verbose_name='Nombre de la cancha',
    )
    cod_interno = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text='Codigo interno de la cancha. Ejemplo: ful-AF321',
        verbose_name='Codigo Interno'
    )
    tiene_vestuario = models.BooleanField(
        default=False,
        help_text='Marque esta opción si la cancha tiene vestuario',
        verbose_name='¿Tiene vestuario?'
    )
    tiene_iluminacion = models.BooleanField(
        default=False,
        help_text='Marque esta opción si la cancha tiene iluminación',
        verbose_name='¿Tiene iluminación?'
    )
    tiene_cesped_sintetico = models.BooleanField(
        default=False,
        help_text='Marque esta opción si la cancha posee césped sintético',
        verbose_name='¿Tiene césped sintético?'
    )

    def get_vestuario(self):
        return 'Sí' if self.tiene_vestuario else 'No'

    def get_iluminacion(self):
        return 'Sí' if self.tiene_iluminacion else 'No'

    def get_cesped(self):
        return 'Sí' if self.tiene_cesped_sintetico else 'No'

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'
        ordering = ['id']


class Reserva(models.Model):
    cliente = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del cliente',
        verbose_name='Nombre del cliente',
    )
    cancha = models.ForeignKey(
        Cancha,
        on_delete=models.CASCADE,
        help_text='Seleccione la cancha que desea reservar',
        verbose_name='Cancha solicitada',
        blank=False,
        null=False
    )
    fecha_turno = models.DateField(
        blank=False,
        null=False,
        help_text='Seleccione la fecha en la que se usará la cancha',
        verbose_name='Fecha del turno'
    )
    hora_turno = models.TimeField(
        blank=False,
        null=False,
        help_text='Ingrese la hora en la que se usará la cancha. ' +
        '(No se pueden transponer).',
        verbose_name='Hora del turno'
    )
    fecha_reserva = models.DateField(
        verbose_name='Fecha de la reserva',
        auto_now_add=True,
    )
    empleado = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        help_text='Empleado que tomó la reserva',
        verbose_name='Empleado de turno'
    )

    def clean(self):
        if self.id:
            reservas = Reserva.objects.filter(
                models.Q(cancha=self.cancha) &
                models.Q(fecha_turno=self.fecha_turno)
            ).exclude(id=self.id)
        else:
            reservas = Reserva.objects.filter(
                models.Q(cancha=self.cancha) &
                models.Q(fecha_turno=self.fecha_turno)
            )
        for reserva in reservas:
            turno = datetime.datetime(
                year=reserva.fecha_turno.year,
                month=reserva.fecha_turno.month,
                day=reserva.fecha_turno.day,
                hour=reserva.hora_turno.hour,
                minute=reserva.hora_turno.minute
            )
            delta_lim_sup = turno + datetime.timedelta(hours=1)
            delta_lim_inf = turno - datetime.timedelta(hours=1)
            turno_nuevo = datetime.datetime(
                year=self.fecha_turno.year,
                month=self.fecha_turno.month,
                day=self.fecha_turno.day,
                hour=self.hora_turno.hour,
                minute=self.hora_turno.minute
            )
            if(turno_nuevo >= delta_lim_inf and turno_nuevo <= delta_lim_sup):
                hora_lim_inf = delta_lim_inf.strftime('%H:%M')
                hora_lim_sup = delta_lim_sup.strftime('%H:%M')
                hora_turno = turno.strftime('%H:%M')
                raise ValidationError(
                    'La hora se traslapa.' +
                    'Ingrese una hora antes de las %(hora_lim_inf)s o ' +
                    'después de las %(hora_lim_sup)s horas.',
                    params={
                        'hora_turno': hora_turno,
                        'hora_lim_sup': hora_lim_sup,
                        'hora_lim_inf': hora_lim_inf
                    }
                )
        return True

    def get_fecha_turno(self):
        return self.fecha_turno.strftime('%d/%m/%Y')

    def get_hora_turno(self):
        return self.hora_turno.strftime('%H:%M:%S')

    def __str__(self):
        return '%s %s' % (self.get_fecha_turno(), self.get_hora_turno())

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha_reserva', 'fecha_turno', 'hora_turno']
