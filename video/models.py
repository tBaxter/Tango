from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Video(models.Model):
    name           = models.CharField(max_length=200)
    video_title    = models.CharField(max_length=200, blank=True, editable=False)
    slug           = models.SlugField(max_length=200, help_text="Will fill itself in")
    poster_frame   = models.FileField(upload_to='video/', blank=True, help_text="Thumbnail to represent movie")
    blurb          = models.TextField(blank=True, null=True)
    video_file     = models.CharField(max_length=255, help_text="Path to M4V or MP4 file", blank=True)
    webm           = models.CharField("WebM", max_length=255, blank=True, null=True, help_text="Path to alternate WebM version for Firefox and Chrome")
    video_width    = models.CharField(max_length=4, blank=True)
    video_height   = models.CharField(max_length=4, blank=True)
    video_at_top   = models.BooleanField("Put video at top", default=False, help_text="If checked, the video will appear preceding the body instead of following.")

    content_type   = models.ForeignKey(ContentType, blank=True, null=True)
    object_id      = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey()

    ustream_id     = models.CharField("Ustream ID", max_length=10, blank=True,
        help_text="""
            If it is an archived ustream video, insert the video ID.
            Do not paste in the embed code.
            The ID is the number at the end of the video URL.
            """
    )
    streaming_url  = models.URLField(blank=True, null=True, help_text="If this is a live streaming Ustream video, give the full URL to the video page.")
    hide_info      = models.BooleanField("Hide title and description", default=False, help_text="If checked, the video title and description will not be shown. Left unchecked, the video will attempt to pull and display the title and description from youtube or Ustream.")
    thumbnail      = models.CharField(blank=True, null=True, max_length=200, editable=False)
    yt_url         = models.CharField("Youtube URL", max_length=200, blank=True, help_text="If it is a youtube video, insert the URL. Do not paste in the embed code.")
    yt_id          = models.CharField('Youtube ID', blank=True, null=True, max_length=50, editable=False)

    def getThumb(self):
        if self.yt_id:
            thumb = "http://img.youtube.com/vi/" + self.yt_id + "/0.jpg"
        else:
            thumb = self.poster_frame  # Do we need to resize?
        return thumb

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/video/%s/' % (self.slug)

    def save(self, *args, **kwargs):
        """We want to store the thumbnail, because it's a good idea."""
        if self.yt_url:
            if self.yt_url.find('&') != -1:
                self.yt_id = self.yt_url[self.yt_url.find("v=") + 2:self.yt_url.find("&")]
            else:
                self.yt_id = self.yt_url[self.yt_url.find("v=") + 2:]
        self.thumbnail = self.getThumb()
        super(Video, self).save(*args, **kwargs)


class VideoGallery(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        help_text="Used for URLs. Will auto-fill, but can be edited with caution."
    )
    gallery_credit = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    video_collection = models.ManyToManyField(Video)

    class Meta:
        verbose_name_plural = "video galleries"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/video/%s/" % (self.slug)
