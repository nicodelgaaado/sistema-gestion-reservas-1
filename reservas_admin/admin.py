from django.contrib import admin
from .models import Reserva

# Register your models here.
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('laboratorio', 'fecha', 'hora_inicio', 'hora_fin', 'usuario', 'estado')
    list_filter = ('estado', 'fecha', 'laboratorio')
    search_fields = ('laboratorio', 'usuario__username', 'motivo')
