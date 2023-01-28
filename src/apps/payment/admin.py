from django.contrib import admin

from apps.donor.models import Donation
from apps.payment.models import Cart, PaymentProvider


# Register your models here.

class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0


class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_provider']
    list_editable = ['is_provider']
    fields = ('is_provider',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount', 'updated_date', 'get_item_counts']
    readonly_fields = ['updated_date', 'get_item_counts']
    fields = ['user', 'amount', 'updated_date', 'get_item_counts']
    inlines = [DonationInline]

    def get_item_counts(self, obj):
        return obj.get_item_counts()

    get_item_counts.short_description = 'Items in the Cart'


admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Cart, CartAdmin)
