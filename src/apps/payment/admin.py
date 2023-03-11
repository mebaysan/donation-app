from django.contrib import admin

from apps.payment.models import (
    Cart,
    PaymentProvider,
    CartItem,
    Donation,
    DonationTransaction,
)
from helpers.template import filters


# Register your models here.


class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ["name", "is_provider"]
    list_editable = ["is_provider"]
    fields = ("is_provider",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "amount", "added_date"]


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ["__str__", "amount", "updated_date", "get_item_counts"]
    readonly_fields = ["updated_date", "get_item_counts"]
    fields = ["user", "amount", "updated_date", "get_item_counts"]
    inlines = [CartItemInline]

    def get_item_counts(self, obj):
        return obj.get_item_counts()

    get_item_counts.short_description = "Items in the Cart"


class DonationAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "donation_item",
        "amount",
        "added_time",
        "get_is_complete_transaction",
    ]
    readonly_fields = [
        "added_time",
        "donation_transaction",
        "user",
        "donation_item",
        "amount",
    ]

    def get_is_complete_transaction(self, obj):
        return "Yes" if obj.is_complete_transaction else "No"

    get_is_complete_transaction.short_description = "Is Transaction Completed"


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ["donation_item", "amount", "user"]

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False


class DonationTransactionAdmin(admin.ModelAdmin):
    inlines = [DonationInline]
    list_display = (
        "__str__",
        "first_name",
        "last_name",
        "email",
        "amount",
        "amount_sent_to_bank",
        "date",
        "status_code_description",
        "status_code",
        "is_complete",
        "group_name",
        "organization_name",
    )
    list_filter = [
        ("is_complete", filters.DropdownFilter),
        ("status_code", filters.DropdownFilter),
        ("group_name", filters.DropdownFilter),
        ("organization_name", filters.DropdownFilter),
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "group_name",
        "organization_name",
    ]
    readonly_fields = [
        "merchant_order_id",
        "amount",
        "amount_sent_to_bank",
        "md_code",
        "is_complete",
        "status_code",
        "status_code_description",
        "user",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "message",
        "donation_platform",
    ]


admin.site.register(DonationTransaction, DonationTransactionAdmin)

admin.site.register(Donation, DonationAdmin)

admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
