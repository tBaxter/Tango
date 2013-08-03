import datetime

from django.conf import settings
from django.db import models


RESTRICT_CONTENT_TO_SITE = getattr(settings, 'RESTRICT_CONTENT_TO_SITE', False)
now = datetime.datetime.now()


class VideoManager(models.Manager):
    """
    If RESTRICT_CONTENT_TO_SITE is True in settings,
    will limit video to current site.

    Usage is simply video.objects.all()
    """
    def get_query_set(self):
        videos = super(VideoManager, self).get_query_set()
        if RESTRICT_CONTENT_TO_SITE:
            videos.filter(sites__id__exact=settings.SITE_ID)
        return videos


class PublishedVideoManager(VideoManager):
    """
    Extends VideoManager to only return videos
    - That are published
    - and have a created date greater than or equal to now.

    Usage is gallery.published.all()
    """
    def get_query_set(self):
        videos = super(PublishedVideoManager, self).get_query_set()
        videos.filter(published=True, created__lte=now)
        return videos
