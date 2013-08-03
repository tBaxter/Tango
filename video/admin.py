from django.contrib import admin
from django.contrib.contenttypes import generic

from .forms import VideoForm
from .models import Video, VideoGallery


class VideoInline(generic.GenericTabularInline):
    """
    Consistent inlined video for other content admin.
    """
    model = Video
    max_num = 2
    extra = 1
    fields = ('url', 'video_at_top', 'hide_info')


class VideoGalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['video_collection']


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'source')
    fieldsets = (
        ('', {'fields': ('url', 'title', 'summary',)}),
        ('Admin fields', {
            'description': 'These should be filled in for you, but you can edit them.',
            'fields': ('slug', ),
            'classes': ['collapse']
        }),
    )


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoGallery, VideoGalleryAdmin)
