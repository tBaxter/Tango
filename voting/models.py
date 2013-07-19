from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from voting.managers import VoteManager

UserModel = getattr(settings, "AUTH_USER_MODEL", "auth.User")

SCORES = (
    ('+1', +1),
    ('-1', -1),
)


class Vote(models.Model):
    user         = models.ForeignKey(UserModel)
    content_type = models.ForeignKey(ContentType)
    object_id    = models.PositiveIntegerField()
    object       = generic.GenericForeignKey('content_type', 'object_id')
    vote         = models.SmallIntegerField(choices=SCORES)

    objects = VoteManager()

    class Meta:
        db_table = 'votes'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = (('user', 'content_type', 'object_id'),)  # Enforce one vote per user per object

    def __unicode__(self):
        return '%s: %s on %s' % (self.user, self.vote, self.object)

    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1
