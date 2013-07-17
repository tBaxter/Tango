from django.contrib import admin
from autotagger.models import AutoTag


class AutoTagAdmin(admin.ModelAdmin):
    fieldsets = (
     ('',      {'fields': ('phrase',)}),
     ('Admin Fields', {
         'fields': ('content_type', 'object_id'), 'classes': ['collapse', ]}),
    )

admin.site.register(AutoTag, AutoTagAdmin)
