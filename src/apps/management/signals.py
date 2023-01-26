from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_donor_group(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name="Donor")
