from django.test import Client,TestCase
from datetime import date, time
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Reserva


class ReservaModelTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='docente', password='clave12345')

    def test_valida_conflicto_horario(self):
        Reserva.objects.create(
            usuario=self.usuario,
            laboratorio='Lab A',
            fecha=date(2026, 5, 7),
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
            motivo='Primera reserva',
        )

        reserva = Reserva(
            usuario=self.usuario,
            laboratorio='Lab A',
            fecha=date(2026, 5, 7),
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
            motivo='Reserva en conflicto',
        )

        with self.assertRaises(ValidationError):
            reserva.full_clean()


class ReservaViewsTest(TestCase):
    def setUp(self):
        self.docentes = Group.objects.get(name='Docente')
        self.usuario = User.objects.create_user(username='docente', password='clave12345')
        self.usuario.groups.add(self.docentes)
        self.client = Client()

    def test_docente_puede_crear_reserva(self):
        self.client.login(username='docente', password='clave12345')
        response = self.client.post(
            reverse('reserva_crear'),
            {
                'laboratorio': 'Lab B',
                'fecha': '2026-05-08',
                'hora_inicio': '08:00',
                'hora_fin': '09:00',
                'motivo': 'Clase practica',
            },
        )
        self.assertRedirects(response, reverse('reserva_lista'))
        self.assertEqual(Reserva.objects.count(), 1)

