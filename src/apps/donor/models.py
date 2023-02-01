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
        return self.image.url

    class Meta:
        verbose_name = 'Donation Item'
        verbose_name_plural = 'Donation Items'

