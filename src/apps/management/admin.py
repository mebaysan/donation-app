from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.http import HttpRequest

from apps.management.models import User, BillAddress, Country, StateProvince

from helpers.template import filters
from helpers.communication.email import send_password_reset_email


class CustomUserAdmin(UserAdmin):
    list_filter = (
        ("is_superuser", filters.DropdownFilter),
        ("is_staff", filters.DropdownFilter),
        ("groups", filters.RelatedDropdownFilter),
        ("is_approved_to_be_in_touch", filters.DropdownFilter),
        ("country", filters.RelatedDropdownFilter),
        ("state_province", filters.RelatedDropdownFilter),
    )
    search_fields = ["username", "first_name", "last_name", "email", "phone_number"]
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_superuser",
    ]
    actions = ["send_password_reset_email_admin_action"]
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            "Additional Data",  # group heading of your choice; set to None for a blank space instead of a header
            {
                "fields": ("phone_number", "gender", "is_approved_to_be_in_touch"),
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "country",
                    "state_province",
                )
            },
        ),
    )

    # the following method executes send_password_reset_email for each user in the queryset
    def send_password_reset_email_admin_action(self, request, queryset):
        for user in queryset:
            send_password_reset_email(user)

    send_password_reset_email_admin_action.short_description = (
        "Send password reset email"
    )


class CustomGroupAdmin(GroupAdmin):
    pass


class BillAddressAdmin(admin.ModelAdmin):
    pass


class StateProvincetInline(admin.TabularInline):
    model = StateProvince
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    inlines = [StateProvincetInline]
    search_fields = ["name", "country_code", "country_code_alpha3", "phone", "currency"]
    list_display = [
        "name",
        "country_code",
        "country_code_alpha3",
        "phone",
        "currency",
        "total_state_province_count",
    ]


admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(BillAddress, BillAddressAdmin)
admin.site.register(Country, CountryAdmin)
