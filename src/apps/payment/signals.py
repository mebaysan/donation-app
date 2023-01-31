from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.donor.models import DonationTransaction
from apps.payment.models import CartItem

User = get_user_model()


@receiver(post_migrate)
def create_base_providers(sender, **kwargs):
    from .models import PaymentProvider
    PaymentProvider.objects.get_or_create(name="KuveytTurk", is_provider=True, code_name='KT')


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    """
        Every user has a cart
    """
    from .models import Cart
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=CartItem)
def update_cart_total_after_save(sender, instance, created, **kwargs):
    """
        Update cart total after a new item added
    """

    instance.cart.update_cart_total()


@receiver(post_delete, sender=CartItem)
def update_cart_total_after_delete(sender, instance, **kwargs):
    """
        Update cart total after a new item added
    """
    instance.cart.update_cart_total()


@receiver(post_save, sender=DonationTransaction)
def clean_cart_after_successfull_payment(sender, instance, created, **kwargs):
    """
        Clean cart if transaction is success and create donation records of cart items
    """
    if instance.is_complete:
        instance.user.cart.clean_cart()
