from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.donor.models import Donation, DonationTransaction


@receiver(post_save, sender=Donation)
def update_cart_total_after_save(sender, instance, created, **kwargs):
    """
        Update cart total after a new item added
    """

    instance.cart.update_cart_total()


@receiver(post_delete, sender=Donation)
def update_cart_total_after_delete(sender, instance, **kwargs):
    """
        Update cart total after a new item added
    """
    instance.cart.update_cart_total()


@receiver(post_save, sender=DonationTransaction)
def clean_cart_after_successfull_payment(sender, instance, created, **kwargs):
    """
        Clean cart if transaction is success
    """
    instance.user.cart.clean_cart()
