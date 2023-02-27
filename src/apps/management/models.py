from django.contrib.auth.models import AbstractUser
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=5)
    country_code_alpha3 = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)
    currency = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class StateProvince(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="state_provinces"
    )

    def __str__(self):
        return self.name


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
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    state_province = models.ForeignKey(
        StateProvince, on_delete=models.CASCADE, null=True, blank=True
    )
    is_approved_to_be_in_touch = models.BooleanField(default=False)

    @property
    def get_total_amount_of_donations(self):
        return (
            self.donation_transactions.filter(is_complete=True).aggregate(
                models.Sum("amount")
            )["amount__sum"]
            or 0
        )

    @property
    def get_total_count_of_donations(self):
        return self.donation_transactions.filter(is_complete=True).count()
