from django.apps import AppConfig


class WasteAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "waste_auth"

    def ready(self):
        import waste_auth.signals
