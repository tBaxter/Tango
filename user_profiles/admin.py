from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=True)
deactivate.short_description = "Deactivate selected users"


class ProfileAdmin(UserAdmin):
    date_hierarchy = 'date_joined'
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    list_display = ('username', 'display_name', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'display_name')
    actions = [deactivate, ]


admin.site.register(Profile, ProfileAdmin)
