from django.contrib import admin
from django.contrib.contenttypes import generic
from video.models import Video, VideoGallery


class VideoInline(generic.GenericTabularInline):
    model = Video
    max_num = 2
    extra = 1
    fields = ('yt_url', 'ustream_id', 'video_at_top',)


class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'content_type', 'object_id')
    fieldsets = (
        ('General info', {'fields': ('name', 'blurb', 'video_at_top', 'ustream_id', 'yt_url')}),
        ('Uploads', {'fields': ('poster_frame', 'video_file', 'webm', 'video_width', 'video_height'), 'classes': ['collapse']}),
        ('Admin info', {'fields': ('slug', 'content_type', 'object_id', 'hide_info'), 'classes': ['collapse']}),
    )


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoGallery)
