from django.contrib import admin

from apps.donor.models import DonationTransaction, Donation, DonationItem, DonationCategory


# Register your models here.

class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)


class DonationItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_published')
    list_editable = ('category', 'is_published',)


class DonationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'donation_item', 'amount', 'added_time')
    readonly_fields = ('added_time',)


class DonationTransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status_code')


admin.site.register(DonationCategory, DonationCategoryAdmin)
admin.site.register(DonationItem, DonationItemAdmin)
admin.site.register(DonationTransaction, DonationTransactionAdmin)
admin.site.register(Donation, DonationAdmin)
