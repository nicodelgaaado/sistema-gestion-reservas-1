from django import forms

from .models import Reserva


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['laboratorio', 'fecha', 'hora_inicio', 'hora_fin', 'motivo']
        widgets = {
            'fecha': DateInput(),
            'hora_inicio': TimeInput(),
            'hora_fin': TimeInput(),
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }


class EstadoReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['estado']


class FiltroReservaForm(forms.Form):
    fecha = forms.DateField(required=False, widget=DateInput())
    laboratorio = forms.CharField(required=False, max_length=100)
