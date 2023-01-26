from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from apps.management.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'Additional Data',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone_number',
                    'gender',
                    'is_approved_to_be_in_touch'
                ),
            },
        ),
        (
            'Location', {
                'fields': (
                    'country',
                    'city',
                    'state'
                )
            }
        )
    )


class CustomGroupAdmin(GroupAdmin):
    pass


admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
