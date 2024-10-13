from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

DONATION_TYPES = (("Dynamic", "Dynamic"), ("Static", "Static"))
CURRENCY_TYPES = (
    ("TRY", "TRY"),
    ("USD", "USD"),
    ("EUR", "EUR"),
)


class DonationCategory(models.Model):
    """
    Holds donation category
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="donation_category/", null=True, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Donation Category"
        verbose_name_plural = "Donation Categories"

    def __str__(self):
        return self.name

    def get_published_items(self):
        return self.items.filter(is_published=True).all()

    def get_image_path(self):
        return self.image.url


class DonationItem(models.Model):
    """
    Holds donation item
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        DonationCategory, on_delete=models.SET_NULL, null=True, related_name="items",
    )
    image = models.ImageField(upload_to="donation_item/", null=True, blank=True)
    is_published = models.BooleanField(default=True)
    # we use the fields below to use restrictions
    donation_type = models.CharField(
        choices=DONATION_TYPES, max_length=7, default="Dynamic"
    )
    quantity_price = models.DecimalField(
        decimal_places=2, max_digits=16, null=True, blank=True
    )
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_image_path(self):
        return self.image.url

    class Meta:
        verbose_name = "Donation Item"
        verbose_name_plural = "Donation Items"


class Bank(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="donation_category/", null=True, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def __str__(self):
        return self.name

    def get_image_path(self):
        return self.image.url


class BankAccount(models.Model):
    account_name = models.CharField(max_length=500, null=True, blank=True)
    account_number = models.CharField(max_length=500, default="", null=True, blank=True)
    branch = models.CharField(max_length=500, null=True, blank=True)
    branch_no = models.IntegerField(null=True, blank=True)
    swift_no = models.CharField(max_length=500, null=True, blank=True)
    iban_no = models.CharField(max_length=500, null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_TYPES, max_length=3)
    description = models.CharField(max_length=500, null=True, blank=True, default="")
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, related_name="bank_accounts"
    )

    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
