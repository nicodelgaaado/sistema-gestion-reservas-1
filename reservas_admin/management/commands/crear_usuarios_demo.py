from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea usuarios demo para probar la aplicacion.'

    def handle(self, *args, **options):
        docente_group, _ = Group.objects.get_or_create(name='Docente')
        admin_group, _ = Group.objects.get_or_create(name='Administrador')

        docente, created_docente = User.objects.get_or_create(username='docente_demo')
        if created_docente:
            docente.set_password('Docente123.')
            docente.save()
        docente.groups.add(docente_group)

        admin_user, created_admin = User.objects.get_or_create(username='admin_demo')
        if created_admin:
            admin_user.set_password('Admin123.')
            admin_user.email = 'admin@example.com'
            admin_user.is_staff = True
            admin_user.save()
        admin_user.groups.add(admin_group)

        self.stdout.write(
            self.style.SUCCESS(
                'Usuarios demo listos: docente_demo / Docente123. y admin_demo / Admin123.'
            )
        )
