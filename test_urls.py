from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^profiles/', include('tango_user.urls')),
    url(r'^video/', include('video.urls')),
)
