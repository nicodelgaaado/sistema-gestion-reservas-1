from django.apps import AppConfig


class ReservasAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas_admin'

    def ready(self):
        import reservas_admin.signals  # noqa: F401
