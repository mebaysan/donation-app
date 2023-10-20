from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError, models

GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
]


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
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    state_province = models.ForeignKey(
        StateProvince, on_delete=models.CASCADE, null=True, blank=True
    )
    is_approved_to_be_in_touch = models.BooleanField(default=False)

    # if there is another user with the same phone number or email or username then it will raise an error
    def save(self, *args, **kwargs):
        if self.email:
            if User.objects.filter(email=self.email).exclude(id=self.id).exists():
                raise IntegrityError("Email already exists")
        if self.username:
            if User.objects.filter(username=self.username).exclude(id=self.id).exists():
                raise IntegrityError("Username already exists")
        if (
            self.phone_number
            and User.objects.filter(phone_number=self.phone_number)
            .exclude(id=self.id)
            .exists()
        ):
            raise IntegrityError("Phone number already exists")
        super().save(*args, **kwargs)

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
