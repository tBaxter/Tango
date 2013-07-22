"""
Overrides Django contrib groups and sites for more control.

Note that model-level changes to these django.contrib apps
are made in tango_admin.models.
"""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

from .admin_actions import nuke_users
from .models import Blacklist


class CustomGroupAdmin(GroupAdmin):
    """
    Custom Groups admin
    Adds "description" field to list display
    """
    list_display = GroupAdmin.list_display + ('description',)


#class CustomSiteAdmin(SiteAdmin):
#    """
#    Custom Site admin
#    Adds fields to list display
#    and breaks content into fieldsets.
#    """
#    list_display = SiteAdmin.list_display + ('description',)


class CustomCommentAdmin(CommentsAdmin):
    list_display = ('user_name', 'comment', 'submit_date', 'is_public')
    actions = [nuke_users]

    def get_actions(self, request):
        actions = super(CommentsAdmin, self).get_actions(request)
        return actions


class BlackListAdmin(admin.ModelAdmin):
    list_display = ['user', 'blacklister', 'reason', 'date']


class TextCounterWidget(forms.Textarea):
    """
    Used for textAreas that need to count their characters
    """
    class Media:
        js = ('/static/admin/text_field_counter.js',)

    def render(self, name, value, attrs=None):
        if attrs:
            attrs['data-counter'] = 'needs_counter'
        else:
            attrs = {'data-counter': 'needs_counter'}
        return super(TextCounterWidget, self).render(name, value, attrs)

#admin.site.unregister(Site)
#admin.site.unregister(Group)
#$admin.site.register(Site, CustomSiteAdmin)
#admin.site.register(Group, CustomGroupAdmin)

admin.site.unregister(Comment)
admin.site.register(Comment, CustomCommentAdmin)

admin.site.register(Blacklist, BlackListAdmin)
