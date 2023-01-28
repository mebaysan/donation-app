from django.apps import AppConfig


class DonorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.donor"

    def ready(self):
        import apps.donor.signals
