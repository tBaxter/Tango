import datetime
import time

from django.db import models

from articles.models import Article
from shared.models import ContentImage

now = datetime.datetime.now()


class Gallery(models.Model):
    overline       = models.CharField(max_length=200, blank=True, null=True)
    title          = models.CharField(max_length=200)
    slug           = models.SlugField(max_length=200, help_text="Used for URLs and identification. Will auto-fill, but can be edited with caution.")
    gallery_credit = models.CharField(max_length=200, blank=True)
    summary        = models.TextField(blank=True)
    created        = models.DateTimeField(auto_now_add=True)
    has_image      = models.CharField(max_length=200, editable=False)
    published      = models.BooleanField(default=True)
    article        = models.ForeignKey(Article, null=True, blank=True)

    class Meta:
        verbose_name_plural = "galleries"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/photos/%s/" % (self.slug)

    def get_image(self):
        try:
            return self.galleryimage_set.all()[0].image
        except:
            return None

    def save(self, *args, **kwargs):
        if self.has_image == "None" or self.has_image is None or self.has_image == '':
            self.has_image = str(self.get_image())
        super(Gallery, self).save(*args, **kwargs)


class GalleryImage(ContentImage):
    gallery  = models.ForeignKey(Gallery)


class BulkImageUpload(models.Model):
    """
    Allows zip or multi-file upload in admin.
    """
    files       = models.FileField(upload_to= "temp/", help_text='Select multiple images or a .zip file of images to upload.')
    gallery     = models.ForeignKey(Gallery)
    caption     = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        for upload_file in self.files:
            upload_file.name = upload_file.name.lower().replace(' ', '_')  # lowercase and replace spaces
            filename = upload_file.name
            if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                # to do: proper dupe checking
                dupe = False
                if not dupe:
                    upload = GalleryImage(
                        gallery         = self.gallery,
                        image           = upload_file,
                        caption         = self.caption,
                    )
                    upload.save()
                    time.sleep(1)
