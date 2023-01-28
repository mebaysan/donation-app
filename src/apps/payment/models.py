from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class PaymentProvider(models.Model):
    name = models.CharField(max_length=255)
    is_provider = models.BooleanField(default=False)

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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    updated_date = models.DateTimeField(auto_now_add=True, auto_created=True)
    donations = models.ManyToManyField('donor.Donation', null=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.user.username
