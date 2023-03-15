from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Donation(models.Model):
    """
    Holds Cart donation items
    """

    donation_item = models.ForeignKey(
        "donor.DonationItem",
        on_delete=models.SET_NULL,
        null=True,
        related_name="donations",
    )
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    added_time = models.DateTimeField(auto_now_add=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    donation_transaction = models.ForeignKey(
        "payment.DonationTransaction",
        on_delete=models.CASCADE,
        related_name="donations",
    )

    def __str__(self):
        return f"{self.user.username}-{self.donation_item.name}-{self.amount}"

    @property
    def is_complete_transaction(self):
        return self.donation_transaction.is_complete


class DonationTransaction(models.Model):
    """
    Holds transaction of donations in the same line with total number
    """

    DONATION_PLATFORMS = [("WEB", "WEB")]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    amount_sent_to_bank = models.CharField(max_length=299)
    merchant_order_id = models.TextField(null=True, blank=True)
    md_code = models.CharField(max_length=300, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status_code = models.CharField(null=True, blank=True, default="-1", max_length=10)
    status_code_description = models.CharField(
        max_length=255, null=True, blank=True, default="Response not received from bank"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="donation_transactions",
    )
    donation_platform = models.CharField(
        choices=DONATION_PLATFORMS, default="WEB", max_length=10
    )
    group_name = models.CharField(max_length=255, null=True, blank=True)
    organization_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Donation Transaction"
        verbose_name_plural = "Donation Transactions"

    def __str__(self):
        return self.merchant_order_id


# Create your models here.
class PaymentProvider(models.Model):
    name = models.CharField(max_length=255)
    is_provider = models.BooleanField(default=False)
    code_name = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Payment Provider"
        verbose_name_plural = "Payment Providers"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_provider:
            published_provider = PaymentProvider.objects.filter(
                is_provider=True
            ).first()
            if published_provider:
                published_provider.is_provider = False
                published_provider.save()
        super(PaymentProvider, self).save(*args, **kwargs)


class CartItem(models.Model):
    donation_item = models.ForeignKey(
        "donor.DonationItem", on_delete=models.SET_NULL, null=True
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    added_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    cart = models.ForeignKey(
        "payment.Cart", on_delete=models.CASCADE, related_name="cart_items"
    )

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    # Eğer sepette item varsa ve tekrar eklenirse var olan item fiyatını güncelle
    # def save(self, *args, **kwargs):
    #     existing_item = CartItem.objects.filter(cart=self.cart, donation_item=self.donation_item).first()
    #     if existing_item:
    #         self.amount += existing_item.amount
    #         existing_item.delete()
    #     super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cart.user.username}-{self.donation_item.name}-{self.amount}"


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_query_name="cart",
        related_name="cart",
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    updated_date = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return self.user.username

    def get_item_counts(self):
        return self.cart_items.count()

    def update_cart_total(self):
        self.amount = 0
        for donation in self.cart_items.all():
            self.amount += donation.amount
        self.save()

    def clean_cart(self):
        self.cart_items.all().delete()
        self.save()
