from django.db import models


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
