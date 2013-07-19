from django.conf.urls import *
from django.views.generic import ListView, DetailView

from video.models import Video, VideoGallery

urlpatterns = patterns(
    '',
    url(
        name="video_gallery_list",
        regex=r'^$',
        view=ListView.as_view(
            queryset=VideoGallery.objects.all(),
            template_name="video/video_list.html",
            context_object_name="video_list",
        )
    ),
    url(
        name='video_gallery_detail',
        regex=r'^gallery/(?P<slug>[-\w]+)/$',
        view=DetailView.as_view(
            queryset=VideoGallery.objects.all(),
            slug_field='slug',
            template_name="video/video_list.html",
            context_object_name="gallery",
        ),
    ),
    url(
        name='video_detail',
        regex=r'^(?P<slug>[-\w]+)/$',
        view=DetailView.as_view(
            queryset=Video.objects.all(),
            slug_field='slug',
            template_name="video/video_detail.html",
            context_object_name="video",
        )
    ),
    url(
        name="video_detail_boxed",
        regex=r'^(?P<slug>[-\w]+)/box/$',
        view=DetailView.as_view(
            queryset=Video.objects.all(),
            slug_field='slug',
            template_name="video/video_detail_boxed.html",
            context_object_name="video"
        )
    ),
)
