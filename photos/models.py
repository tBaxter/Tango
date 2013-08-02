import datetime
import time

from django.db import models

from articles.models import Article
from tango_shared.models import ContentImage

now = datetime.datetime.now()


class Gallery(models.Model):
    overline = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        help_text="""Used for URLs and identification.
        Will auto-fill, but can be edited with caution.
        """
    )
    credit = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    published = models.BooleanField(default=True)
    article = models.ForeignKey(Article, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    has_image = models.BooleanField(max_length=200, default=False, editable=False)

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


class BulkImageUpload(models.Model):
    """
    Allows multi-file upload in admin.
    """
    files       = models.FileField(upload_to= "temp/", help_text='Select multiple images or a .zip file of images to upload.')
    gallery     = models.ForeignKey(Gallery)
    caption     = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        for f in self.files:
            clean_file_name = f.name.lower().replace(' ', '_')  # lowercase and replace spaces
            print clean_file_name
            if clean_file_name.endswith('.jpg') or clean_file_name.endswith('.jpeg'):
                # to do: proper dupe checking
                dupe = False
                if not dupe:
                    print 'upload starting'
                    upload = GalleryImage(
                        gallery         = self.gallery,
                        image           = clean_file_name,
                        caption         = self.caption,
                    )
                    upload.save()
                    time.sleep(1)
