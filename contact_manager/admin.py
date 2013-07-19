
from django.contrib import admin

from .models import Recipient, Contact, ContactFormController
from .forms import ContactForm
#from supersites.admin_actions import remove_bad_users


def publish_selected(modeladmin, request, queryset):
    rows_updated = queryset.update(publish=True)
    if rows_updated == 1:
        message_bit = "One item was"
    else:
        message_bit = "%s items were" % rows_updated
    modeladmin.message_user(request, "%s published." % message_bit)
publish_selected.short_description = "Publish"


def unpublish_selected(modeladmin, request, queryset):
    rows_updated = queryset.update(publish=False)
    if rows_updated == 1:
        message_bit = "One item was"
    else:
        message_bit = "%s items were" % rows_updated
    modeladmin.message_user(request, "%s unpublished." % message_bit)
unpublish_selected.short_description = "Unpublish"


class RecipientInline(admin.TabularInline):
    model = Recipient


class ContactFormControllerAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')
    filter_horizontal = ('recipients', 'other_recipients')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('The Form', {
            'fields': (
                'name',
                'request_contact_info',
                'allow_uploads',
                'limit_words',
                'override_subject',
                'subject_label',
                'body_label'
            )
        }),
        ('Routing', {
            'fields': (
                'store_in_db', ('send_emails', 'email_options')
            )
        }),
        ('Recipients', {
            'fields': ('recipients', 'other_recipients')
        }),
        ('Custom content', {
            'fields': ('pre_form_msg', 'thank_you'),
            'classes': ['collapse', ]
        }),
        ('Admin fields', {
            'fields': ('slug', 'site', 'require_auth'),
            'classes': ['collapse', ]
        }),
    )


class ContactAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'controller', 'subject', 'summary', 'submitted', 'has_photo', 'publish')
    # To-Do: add remove_bad_users to actions when it can be safely imported.
    actions = [publish_selected, unpublish_selected]
    list_filter = ('publish', 'site', 'controller')
    date_hierarchy = 'submitted'
    search_fields = ['sender_email', 'sender_name']


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'found_on_form')


admin.site.register(ContactFormController, ContactFormControllerAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Recipient, RecipientAdmin)
