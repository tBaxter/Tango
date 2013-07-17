from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class AutoTag(models.Model):
    """
    Stores a given tag that should be searched for.
    Plus an optional object it should be matched with.
    Via autotagging, it will establish relationships between content
    matching the given phrase.
    """
    phrase   = models.CharField(max_length=200, help_text="""
                    The phrase you want to search for.
                    IMPORTANT: be sure your phrase won't create false positives.
                    For example, Attempting to tag 'Django' would also tag 'Django Reinhardt', 'Django Unchained',
                    and any other instance of the phrase.
                    """)
    articles       = models.ManyToManyField('articles.Article', blank=True, null=True, editable=False)
    content_type   = models.ForeignKey(ContentType, blank=True, null=True)
    object_id      = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.phrase
