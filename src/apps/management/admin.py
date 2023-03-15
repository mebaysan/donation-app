from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from apps.management.models import User

from helpers.template import filters


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


class CustomGroupAdmin(GroupAdmin):
    pass


admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
