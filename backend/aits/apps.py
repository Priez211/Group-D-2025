from django.apps import AppConfig


class AitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aits'
    def ready(self):
        import aits.signals
