from django.conf.urls import patterns, url
from django.views.generic import DetailView

from .models import Video

urlpatterns = patterns(
    '',
    url(
        name="video_list",
        regex=r'^$',
        view='video.views.video_list'
    ),
    url(
        name="video_gallery_list",
        regex=r'^galleries/$',
        view='video.views.video_gallery_list'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        name='video_detail',
        view='video.views.video_detail'
    ),
    url(
        regex=r'^gallery/(?P<slug>[-\w]+)/$',
        name='video_gallery_detail',
        view='video.views.video_gallery_detail'
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
