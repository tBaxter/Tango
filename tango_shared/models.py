import datetime

from PIL import Image

from django.db import models
from django.utils.safestring import mark_safe

from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer

now = datetime.datetime.now()


def set_img_path(instance, filename):
    """
    Sets upload_to dynamically
    """
    upload_path = '/'.join(['img', instance._meta.app_label, str(now.year), str(now.month), filename])
    return upload_path


class ContentImage(models.Model):
    """
    Generic image object, to be attached to other content.
    It is abstract, and must be subclassed.
    To do -- figure out per-model img_path
    """
    image = ThumbnailerImageField(
        upload_to = set_img_path,
        help_text = "Image size should be a minimum of 720px and no more than 2000px (width or height)",
        blank=True
    )
    caption = models.CharField(max_length=255, blank=True)
    byline = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(
        blank=True,
        null=True,
        help_text="For manual sorting."
    )
    thumb = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        editable=False
    )
    is_vertical = models.BooleanField(blank=True, default=False, editable=False)

    class Meta:
        ordering = ['order', '-id']
        abstract = True

    def __unicode__(self):
        return mark_safe(self.admin_thumb())

    def save(self, *args, **kwargs):
        """
        We want to do dimension checks and/or resizing BEFORE the original image is saved.
        Note that if we can't get image dimensions, it's considered an invalid image
        and we return without saving.
        If the image has changed, sets self.thumb to None, triggering post_save thumbnailer.
        """
        img = self.image
        # Check if this is an already existing photo
        try:
            old_self = self.__class__.objects.get(id=self.id)
        except:
            old_self = None
        #  Run on new and changed images:
        if self.id is None or self.thumb is None or (old_self.image != img):
            try:
                height = img.height
                width  = img.width
            except Exception, inst:
                # We aren't dealing with a reliable image, so....
                print "Error saving... Unable to get image height or width: %s" % inst
                return
            # If image is vertical or square (treated as vertical)...
            if height >= width:
                self.vertical = True
            if width > 900 or height > 1200:
                """
                The image is larger than we want.
                We're going to downsize it BEFORE it is saved,
                using PIL on the InMemoryUploadedFile.
                """
                image = Image.open(img)
                image.resize((900, 1200), Image.ANTIALIAS)
                image.save(img.path)
            try:
                ezthumb_field = get_thumbnailer(self.image)
                self.thumb = ezthumb_field.get_thumbnail({
                    'size': (80, 80),
                    'crop': ',-10'
                }).url.replace("\\", "/")
            except Exception, inst:
                print "Error thumbnailing %s: %s" % (self.id, inst)
        super(ContentImage, self).save(*args, **kwargs)

    def admin_thumb(self):
        """
        Allows for admin thumbnails
        """
        if self.thumb:
            return '<img src="%s">' % self.thumb
        return None
    admin_thumb.allow_tags = True
