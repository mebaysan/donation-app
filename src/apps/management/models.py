from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MALE = "Male"
    FEMALE = "Female"
    GENDER_IN_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True
    )
    country = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    is_approved_to_be_in_touch = models.BooleanField(default=False)
