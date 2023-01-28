from django.contrib import admin

from apps.payment.models import Cart, PaymentProvider


# Register your models here.

class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_provider']
    list_editable = ['is_provider']
    fields = ('is_provider',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'amount', 'updated_date']


admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Cart, CartAdmin)
