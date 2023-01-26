from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_base_providers(sender, **kwargs):
    from .models import PaymentProvider
    PaymentProvider.objects.get_or_create(name="KuveytTurk")
