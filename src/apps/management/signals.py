from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_migrate)
def create_donor_group(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name="Donor")


@receiver(post_save, sender=User)
def add_user_into_donor_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group
    group = Group.objects.filter(name="Donor").first()
    if created:
        instance.groups.add(group)
        instance.save()
