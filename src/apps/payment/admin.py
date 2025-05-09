from django.contrib import admin

from apps.payment.models import (
    Cart,
    PaymentProvider,
    CartItem,
    Donation,
    DonationTransaction,
)
from helpers.template import filters
from helpers.http.writers import get_csv_response_of_queryset
from rangefilter.filters import DateRangeFilterBuilder, DateTimeRangeFilterBuilder
from datetime import datetime


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
    actions = ["export_to_csv", "export_all_to_csv"]

    def get_is_complete_transaction(self, obj):
        return "Yes" if obj.is_complete_transaction else "No"

    get_is_complete_transaction.short_description = "Is Transaction Completed"

    def export_to_csv(self, request, queryset):
        """
        Export the selected donations to CSV
        """
        res = get_csv_response_of_queryset(queryset, "donations")
        return res

    export_to_csv.short_description = "Export Donations to CSV"

    def export_all_to_csv(self, request, *args, **kwargs):
        """
        Export all donations to CSV
        """
        queryset = Donation.objects.all()
        res = get_csv_response_of_queryset(queryset, "donations")
        return res

    export_all_to_csv.short_description = "Export All Donations to CSV"


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
        (
            "date",
            DateTimeRangeFilterBuilder(
                title="Date",
            ),
        ),
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
        "client_ip_address",
        "country",
        "country_code",
        "state_province",
        "state_code",
        "add_line",
        "postal_code",
    ]
    actions = ["export_to_csv", "export_all_to_csv"]

    def export_to_csv(self, request, queryset):
        """
        Export the selected donation transactions to CSV
        """
        res = get_csv_response_of_queryset(queryset, "donation_transactions")
        return res

    export_to_csv.short_description = "Export Donation Transactions to CSV"

    def export_all_to_csv(self, request, *args, **kwargs):
        """
        Export all donation transactions to CSV
        """
        queryset = DonationTransaction.objects.all()
        res = get_csv_response_of_queryset(queryset, "donation_transactions")
        return res

    export_all_to_csv.short_description = "Export All Donation Transactions to CSV"


admin.site.register(DonationTransaction, DonationTransactionAdmin)

admin.site.register(Donation, DonationAdmin)

admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
