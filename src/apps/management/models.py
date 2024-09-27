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

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    @property
    def total_state_province_count(self):
        return self.state_provinces.count()


class StateProvince(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="state_provinces"
    )
    state_code = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = "StateProvince"
        verbose_name_plural = "StateProvinces"

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


class BillAddress(models.Model):
    address_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state_province = models.ForeignKey(StateProvince, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_code = models.CharField(max_length=255, blank=True)
    add_line = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Bill Address"
        verbose_name_plural = "Bill Addresses"

    def __str__(self):
        return f"{self.user.username} - {self.address_name}"
