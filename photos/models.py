import datetime

from django.db import models

from .managers import GalleryManager, PublishedGalleryManager
from tango_shared.models import ContentImage, BaseContentModel

now = datetime.datetime.now()


class Gallery(BaseContentModel):
    credit = models.CharField(max_length=200, blank=True)
    article = models.ForeignKey('articles.Article', null=True, blank=True)
    has_image = models.BooleanField(max_length=200, default=False, editable=False)
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

    def save(self, *args, **kwargs):
        if self.pk and not self.has_image:
            if self.get_image():
                self.has_image = True
        super(Gallery, self).save(*args, **kwargs)


class GalleryImage(ContentImage):
    gallery  = models.ForeignKey(Gallery)
