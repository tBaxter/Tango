import datetime

from django.conf import settings
from django.db import models


RESTRICT_CONTENT_TO_SITE = getattr(settings, 'RESTRICT_CONTENT_TO_SITE', False)
now = datetime.datetime.now()


class GalleryManager(models.Manager):
    """
    Custom gallery objects manager.
    If RESTRICT_CONTENT_TO_SITE is True in settings,
    will limit galleries to current site.

    Usage is simply gallery.objects.all()
    """
    def get_query_set(self):
        galleries = super(GalleryManager, self).get_query_set()
        if RESTRICT_CONTENT_TO_SITE:
            galleries.filter(sites__id__exact=settings.SITE_ID)
        return galleries


class PublishedGalleryManager(GalleryManager):
    """
    Extends GalleryManager to only return galleries
    - That are published
    - With a pub_date greater than or equal to now.

    Usage is gallery.published.all()
    """
    def get_query_set(self):
        galleries = super(PublishedGalleryManager, self).get_query_set()
        galleries.filter(published=True, created__lte=now)
        return galleries
