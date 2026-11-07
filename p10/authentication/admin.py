from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin[User]):
    # Les fieldsets natifs ignorent les champs ajoutés : on les expose dans une section dédiée.
    fieldsets: Any = (*(BaseUserAdmin.fieldsets or ()), ('SoftDesk', {
        'fields': ('age', 'can_be_contacted', 'can_data_be_shared'),
    }))
    add_fieldsets: Any = (*BaseUserAdmin.add_fieldsets, ('SoftDesk', {
        'fields': ('email', 'age', 'can_be_contacted', 'can_data_be_shared'),
    }))
