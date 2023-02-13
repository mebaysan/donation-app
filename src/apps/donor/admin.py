from django.contrib import admin

from apps.donor.models import DonationItem, DonationCategory


# Register your models here.

class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


class DonationItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_published', 'donation_type')
    list_editable = ('category', 'is_published',)


admin.site.register(DonationCategory, DonationCategoryAdmin)
admin.site.register(DonationItem, DonationItemAdmin)
