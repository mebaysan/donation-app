from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_migrate)
def create_base_providers(sender, **kwargs):
    from .models import PaymentProvider
    PaymentProvider.objects.get_or_create(name="KuveytTurk")


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    """
        Every user has a cart
    """
    from .models import Cart
    if created:
        Cart.objects.create(user=instance)
