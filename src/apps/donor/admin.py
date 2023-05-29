from django.contrib import admin

from apps.donor.models import DonationItem, DonationCategory, Bank, BankAccount
from apps.payment.models import Donation


# Register your models here.


class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "order",)
    list_editable = ("is_published", "order",)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            donation_items = DonationItem.objects.filter(category_id=obj.id).all()
            donations = Donation.objects.filter(
                donation_item__in=donation_items
            ).count()
            if donations != 0:
                return False
            else:
                return True


class DonationItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_published", "donation_type")
    list_editable = (
        "category",
        "is_published",
    )

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if obj.donations.count() != 0:
                return False
            else:
                return True


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1


class BankAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]
    list_display = [
        "name",
        "is_published",
    ]
    list_editable = [
        "is_published",
    ]


class BankAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(DonationCategory, DonationCategoryAdmin)
admin.site.register(DonationItem, DonationItemAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
