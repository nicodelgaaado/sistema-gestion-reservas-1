from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


class Reserva(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APROBADA = 'aprobada'
    ESTADO_RECHAZADA = 'rechazada'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADA, 'Aprobada'),
        (ESTADO_RECHAZADA, 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    laboratorio = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    motivo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', 'hora_inicio']

    def __str__(self):
        return f'{self.laboratorio} - {self.fecha} ({self.get_estado_display()})'

    def puede_editarse(self):
        return self.estado == self.ESTADO_PENDIENTE

    def clean(self):
        super().clean()
        if self.hora_inicio and self.hora_fin and self.hora_inicio >= self.hora_fin:
            raise ValidationError('La hora de inicio debe ser menor que la hora de fin.')

        if self.fecha and self.laboratorio and self.hora_inicio and self.hora_fin:
            conflicto = (
                Reserva.objects.filter(
                    laboratorio__iexact=self.laboratorio.strip(),
                    fecha=self.fecha,
                )
                .exclude(pk=self.pk)
                .exclude(estado=self.ESTADO_RECHAZADA)
                .filter(Q(hora_inicio__lt=self.hora_fin) & Q(hora_fin__gt=self.hora_inicio))
            )
            if conflicto.exists():
                raise ValidationError(
                    'Ya existe una reserva en ese laboratorio para el rango horario seleccionado.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


