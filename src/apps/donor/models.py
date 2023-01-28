from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class DonationCategory(models.Model):
    """
            Holds donation category
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='donation_category/', null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Donation Category'
        verbose_name_plural = 'Donation Categories'

    def __str__(self):
        return self.name

    def get_published_items(self):
        return self.items.filter(is_published=True).all()


class DonationItem(models.Model):
    """
        Holds donation item
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(DonationCategory, on_delete=models.SET_NULL, null=True, related_name='items')
    image = models.ImageField(upload_to='donation_item/', null=True, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_image_path(self):
        if settings.DEBUG == 1:
            return self.image.url
        else:
            # todo: implement s3
            pass

    class Meta:
        verbose_name = 'Donation Item'
        verbose_name_plural = 'Donation Items'


class Donation(models.Model):
    """
        Holds Cart donation items
    """
    donation_item = models.ForeignKey(DonationItem, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    cart = models.ForeignKey('payment.Cart', on_delete=models.CASCADE, null=True, related_query_name='donations',
                             related_name='donations')

    def save(self, *args, **kwargs):
        super(Donation, self).save(*args, **kwargs)


class DonationTransaction(models.Model):
    """
        Holds transaction of donations in the same line with total number
    """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=16)
    merchant_order_id = models.TextField(null=True, blank=True)
    md_code = models.CharField(max_length=300, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status_code = models.CharField(null=True, blank=True, default="-1", max_length=3)
    status_code_description = models.CharField(
        max_length=255, null=True, blank=True, default="Response not received from bank"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    donations = models.ManyToManyField(Donation)

    class Meta:
        verbose_name = 'Donation Transaction'
        verbose_name_plural = 'Donation Transactions'
