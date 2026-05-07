import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import EstadoReservaForm, FiltroReservaForm, ReservaForm
from .models import Reserva


def usuario_es_administrador(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='Administrador').exists()
    )


def usuario_es_docente(user):
    return user.is_authenticated and user.groups.filter(name='Docente').exists()


class InicioSesionView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class InicioView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_reservas = Reserva.objects.count()
        reservas_pendientes = Reserva.objects.filter(estado=Reserva.ESTADO_PENDIENTE).count()
        reservas_aprobadas = Reserva.objects.filter(estado=Reserva.ESTADO_APROBADA).count()
        laboratorios_activos = (
            Reserva.objects.values('laboratorio').distinct().count()
        )

        context.update(
            {
                'total_reservas': total_reservas,
                'reservas_pendientes': reservas_pendientes,
                'reservas_aprobadas': reservas_aprobadas,
                'laboratorios_activos': laboratorios_activos,
                'es_administrador': usuario_es_administrador(self.request.user),
                'es_docente': usuario_es_docente(self.request.user),
            }
        )
        return context


class CierreSesionView(LogoutView):
    next_page = reverse_lazy('login')


class DocenteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return usuario_es_docente(self.request.user)


class AdministradorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return usuario_es_administrador(self.request.user)


class RolSistemaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return usuario_es_docente(self.request.user) or usuario_es_administrador(self.request.user)


class ReservaQuerysetMixin(RolSistemaRequiredMixin):
    filtro_form = None

    def get_base_queryset(self):
        queryset = Reserva.objects.select_related('usuario')
        if usuario_es_administrador(self.request.user):
            return queryset
        return queryset.filter(usuario=self.request.user)

    def get_filtered_queryset(self):
        queryset = self.get_base_queryset()
        self.filtro_form = FiltroReservaForm(self.request.GET or None)
        if self.filtro_form.is_valid():
            fecha = self.filtro_form.cleaned_data.get('fecha')
            laboratorio = self.filtro_form.cleaned_data.get('laboratorio')
            if fecha:
                queryset = queryset.filter(fecha=fecha)
            if laboratorio:
                queryset = queryset.filter(laboratorio__icontains=laboratorio)
        return queryset


class ReservaListView(ReservaQuerysetMixin, ListView):
    model = Reserva
    template_name = 'reservas_admin/reserva_list.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object_list
        context['filtro_form'] = self.filtro_form
        context['total_reservas'] = queryset.count()
        context['estadisticas_laboratorio'] = queryset.values('laboratorio').annotate(
            total=Count('id')
        ).order_by('-total', 'laboratorio')
        context['estadisticas_estado'] = queryset.values('estado').annotate(
            total=Count('id')
        ).order_by('estado')
        context['es_administrador'] = usuario_es_administrador(self.request.user)
        context['es_docente'] = usuario_es_docente(self.request.user)
        return context


class ReservaCreateView(DocenteRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas_admin/reserva_form.html'
    success_url = reverse_lazy('reserva_lista')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'La reserva fue creada correctamente.')
        return super().form_valid(form)


class ReservaUpdateView(DocenteRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas_admin/reserva_form.html'
    success_url = reverse_lazy('reserva_lista')

    def dispatch(self, request, *args, **kwargs):
        reserva = self.get_object()
        if not reserva.puede_editarse():
            messages.error(request, 'Solo se pueden editar reservas en estado pendiente.')
            return redirect('reserva_lista')
        if reserva.usuario != request.user:
            messages.error(request, 'No tienes permiso para editar esta reserva.')
            return redirect('reserva_lista')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue actualizada correctamente.')
        return super().form_valid(form)


class ReservaDeleteView(DocenteRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'reservas_admin/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva_lista')

    def dispatch(self, request, *args, **kwargs):
        reserva = self.get_object()
        if not reserva.puede_editarse():
            messages.error(request, 'Solo se pueden eliminar reservas en estado pendiente.')
            return redirect('reserva_lista')
        if reserva.usuario != request.user:
            messages.error(request, 'No tienes permiso para eliminar esta reserva.')
            return redirect('reserva_lista')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'La reserva fue eliminada correctamente.')
        return super().form_valid(form)


class CambiarEstadoReservaView(AdministradorRequiredMixin, UpdateView):
    model = Reserva
    form_class = EstadoReservaForm
    template_name = 'reservas_admin/reserva_estado_form.html'
    success_url = reverse_lazy('reserva_lista')

    def form_valid(self, form):
        messages.success(self.request, 'El estado de la reserva fue actualizado.')
        return super().form_valid(form)


class ExportarReservasCSVView(ReservaQuerysetMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = self.get_filtered_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reservas.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ['Usuario', 'Laboratorio', 'Fecha', 'Hora inicio', 'Hora fin', 'Estado', 'Motivo']
        )
        for reserva in queryset:
            writer.writerow(
                [
                    reserva.usuario.username,
                    reserva.laboratorio,
                    reserva.fecha,
                    reserva.hora_inicio,
                    reserva.hora_fin,
                    reserva.get_estado_display(),
                    reserva.motivo,
                ]
            )
        return response
