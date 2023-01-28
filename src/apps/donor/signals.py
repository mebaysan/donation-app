from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.donor.models import Donation


@receiver(post_save, sender=Donation)
def update_cart_total_after_save(sender, instance, created, **kwargs):
    """
        Update cart total after a new item added
    """

    instance.cart.amount = 0
    for donation in instance.cart.donations.all():
        instance.cart.amount += donation.amount
    instance.cart.save()


@receiver(post_delete, sender=Donation)
def update_cart_total_after_delete(sender, instance, **kwargs):
    """
        Update cart total after a new item added
    """

    instance.cart.amount = 0
    for donation in instance.cart.donations.all():
        instance.cart.amount += donation.amount
    instance.cart.save()
