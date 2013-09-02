from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from .helpers import get_youtube_data, get_vimeo_data, get_ustream_data
from .managers import VideoManager, PublishedVideoManager

from tango_shared.models import BaseContentModel


class Video(BaseContentModel):
    video_at_top = models.BooleanField(
        "Put video at top",
        default=False,
        help_text="""
            If checked, the video will appear preceding the body
            of any related content instead of following.
            """
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        help_text=""""
            Acceptable sources are Youtube, Vimeo and Ustream.
            Please give the link URL, not the embed code.
            """
    )
    hide_info = models.BooleanField(
        "Hide title and description",
        default=False,
        help_text="""
            If checked, the video title and description will not be shown.
            Left unchecked, the video will attempt to display the title and description
            from the video source.
            """
    )

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey()

    key = models.CharField(max_length=20, blank=True, editable=False)
    source = models.CharField(max_length=20, blank=True, editable=False)
    embed_src = models.CharField(max_length=200, blank=True, editable=False)
    thumb_url = models.CharField(max_length=200, blank=True, editable=False)

    # Managers
    objects   = VideoManager()
    published = PublishedVideoManager()

    def __unicode__(self):
        return '{}: {}'.format(self.source, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('video_detail', [self.slug])

    def save(self, *args, **kwargs):
        if not self.embed_src:
            if 'youtube.com/watch' in self.url or 'youtu.be/' in self.url:
                self = get_youtube_data(self)

            if 'vimeo.com/' in self.url:
                self = get_vimeo_data(self)

            if 'ustream.tv/' in self.url:
                self = get_ustream_data(self)

        if self.key and self.embed_src:
            self.embed_src = """
                <iframe src="{}{}" height="360" width="100%%"></iframe>
                """.format(self.embed_src, self.key)
        super(Video, self).save()

    def get_image(self):
        return self.thumb_url


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

    @models.permalink
    def get_absolute_url(self):
        return ('video_gallery_detail', [self.slug])
