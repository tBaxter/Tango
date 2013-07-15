from django.contrib import admin

from .forms import BulkUploadForm
from .models import Gallery, GalleryImage, BulkImageUpload


def make_published(self, request, queryset):
    rows_updated = queryset.update(published=True)
    if rows_updated == 1:
        message_bit = "1 gallery was"
    else:
        message_bit = "%s galleries were" % rows_updated
    self.message_user(request, "%s published." % message_bit)
make_published.short_description = "Publish"


def make_unpublished(self, request, queryset):
    rows_updated = queryset.update(published=False)
    if rows_updated == 1:
        message_bit = "1 gallery was"
    else:
        message_bit = "%s galleries were" % rows_updated
    self.message_user(request, "%s unpublished." % message_bit)
make_unpublished.short_description = "Unpublish"


class GalleryInline(admin.TabularInline):
    model = GalleryImage
    extra = 10


class BulkUploadInline(admin.TabularInline):
    model = BulkImageUpload
    extra = 1
    form = BulkUploadForm


class BulkUploadAdmin(admin.ModelAdmin):
    form = BulkUploadForm


class GalleryAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/admin/inline_reorder.js',)

    ordering = ['-created']
    actions = [make_published, make_unpublished]

    list_display = ('title', 'gallery_credit', 'published', 'created',)
    list_filter = ('published', 'article')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'summary']

    inlines = [
        BulkUploadInline,
        GalleryInline,
    ]

    fieldsets = (
        ('Header', {'fields': ('overline', 'title')}),
        ('Content', {'fields': ('summary', 'article')}),
        ('Meta', {'fields': ('gallery_credit', 'published')}),
        ('Admin fields', {
            'description': 'You should rarely, if ever, need to touch these fields.',
            'fields': ('slug',),
            'classes': ['collapse']
        }),
    )


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'gallery', 'caption', 'byline', )
    search_fields = ['gallery__title', 'caption', 'byline']
    list_filter = ('gallery',)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(BulkImageUpload, BulkUploadAdmin)
