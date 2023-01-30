from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from apps.donor.models import Donation

User = get_user_model()


# Create your models here.
class PaymentProvider(models.Model):
    name = models.CharField(max_length=255)
    is_provider = models.BooleanField(default=False)

    # todo: implement creating donations after successfull transaction

    class Meta:
        verbose_name = 'Payment Provider'
        verbose_name_plural = 'Payment Providers'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_provider:
            published_provider = PaymentProvider.objects.filter(is_provider=True).first()
            if published_provider:
                published_provider.is_provider = False
                published_provider.save()
        super(PaymentProvider, self).save(*args, **kwargs)


class CartItem(models.Model):
    donation_item = models.ForeignKey('donor.DonationItem', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    added_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    cart = models.ForeignKey('payment.Cart', on_delete=models.CASCADE, related_name='cart_items')

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def save(self, *args, **kwargs):
        existing_item = CartItem.objects.filter(cart=self.cart, donation_item=self.donation_item).first()
        if existing_item:
            self.amount += existing_item.amount
            existing_item.delete()
        super(CartItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cart.user.username}-{self.donation_item.name}-{self.amount}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_query_name='cart',
                                related_name='cart')
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    updated_date = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

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
        cart_items = self.cart_items.all()
        for cart_item in cart_items:
            new_donation = Donation.objects.create(
                donation_item=cart_item.donation_item, amount=cart_item.amount, added_time=datetime.now(),
                user=cart_item.cart.user)
            new_donation.save()
        self.cart_items.all().delete()
        self.save()
