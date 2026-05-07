from django.urls import path

from .views import (
    CambiarEstadoReservaView,
    CierreSesionView,
    ExportarReservasCSVView,
    InicioSesionView,
    ReservaCreateView,
    ReservaDeleteView,
    ReservaListView,
    ReservaUpdateView,
)

urlpatterns = [
    path('login/', InicioSesionView.as_view(), name='login'),
    path('logout/', CierreSesionView.as_view(), name='logout'),
    path('reservas/', ReservaListView.as_view(), name='reserva_lista'),
    path('reservas/nueva/', ReservaCreateView.as_view(), name='reserva_crear'),
    path('reservas/<int:pk>/editar/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('reservas/<int:pk>/eliminar/', ReservaDeleteView.as_view(), name='reserva_eliminar'),
    path('reservas/<int:pk>/estado/', CambiarEstadoReservaView.as_view(), name='reserva_estado'),
    path('reservas/exportar/csv/', ExportarReservasCSVView.as_view(), name='reserva_exportar_csv'),
]
