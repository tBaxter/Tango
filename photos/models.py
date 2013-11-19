from django.conf import settings
from django.db import models

from .managers import GalleryManager, PublishedGalleryManager
from tango_shared.models import ContentImage, BaseContentModel

supports_articles = 'articles' in settings.INSTALLED_APPS


class Gallery(BaseContentModel):
    credit = models.CharField(max_length=200, blank=True)
    published = models.BooleanField(default=True)
    
    if supports_articles:
        article = models.ForeignKey('articles.Article', blank=True, null=True)

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
            return self.galleryimage_set.all()[0]
        except IndexError:
            return None


class GalleryImage(ContentImage):
    gallery  = models.ForeignKey(Gallery)
