import datetime

from django.db import models

from .managers import GalleryManager, PublishedGalleryManager
from tango_shared.models import ContentImage, BaseContentModel

now = datetime.datetime.now()


class Gallery(BaseContentModel):
    credit = models.CharField(max_length=200, blank=True)
    article = models.ForeignKey('articles.Article', null=True, blank=True)
    published = models.BooleanField(default=True)

    # Managers
    objects   = GalleryManager()
    published = PublishedGalleryManager()

    class Meta:
        verbose_name_plural = "galleries"

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('gallery_detail', [self.slug])

    def get_image(self):
        try:
            return self.galleryimage_set.all()[0].image
        except IndexError:
            return None


class GalleryImage(ContentImage):
    gallery  = models.ForeignKey(Gallery)
