from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile
from .forms import ProfileCreationForm


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=True)
deactivate.short_description = "Deactivate selected users"


class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm

    date_hierarchy = 'date_joined'
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    list_display = ('username', 'display_name', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'display_name')
    actions = [deactivate, ]


    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(ProfileAdmin, self).get_form(request, obj, **defaults)

admin.site.register(Profile, ProfileAdmin)
