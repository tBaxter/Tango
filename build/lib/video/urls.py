from django.conf.urls import patterns, url

urlpatterns = patterns(
    'video.views',
    url(
        name="video_list",
        regex=r'^$',
        view='video_list'
    ),
    url(
        name="video_gallery_list",
        regex=r'^galleries/$',
        view='video_gallery_list'
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        name='video_detail',
        view='video_detail'
    ),
    url(
        regex=r'^gallery/(?P<slug>[-\w]+)/$',
        name='video_gallery_detail',
        view='video_gallery_detail'
    ),
)
