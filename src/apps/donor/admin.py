from django.contrib import admin

from apps.donor.models import DonationItem, DonationCategory, Bank, BankAccount
from apps.payment.models import Donation


class DonationItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "is_published", "donation_type", "order")
    list_editable = ("category", "is_published", "order")

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if obj.donations.count() != 0:
                return False
            else:
                return True


class DonationItemInline(admin.TabularInline):
    model = DonationItem
    extra = 1


class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
        "order",
    )
    list_editable = (
        "is_published",
        "order",
    )
    inlines = [DonationItemInline]

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


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1


class BankAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]
    list_display = [
        "name",
        "is_published",
        "order",
    ]
    list_editable = [
        "is_published",
        "order",
    ]


class BankAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(DonationCategory, DonationCategoryAdmin)
admin.site.register(DonationItem, DonationItemAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(BankAccount, BankAccountAdmin)
