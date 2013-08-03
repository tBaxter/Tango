from django.conf import settings
#from django.contrib.sites.models import Site
#from django.contrib.auth.models import Group
from django.db import models

UserModel = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# Add some description and featured to Site and auth.Group models
#Site.add_to_class('description', models.CharField(
#    max_length=100,
#    blank=True,
#    help_text='A brief description to differentiate this site.')
#)

#Group.add_to_class('description', models.TextField(
#    blank=True,
#    help_text='A brief description of this group')
#)


class Blacklist(models.Model):
    user = models.ForeignKey(UserModel, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    blacklister = models.ForeignKey(UserModel, editable=False, related_name="blacklister")
    reason = models.TextField(help_text="""
        The reason for the blacklist, for our records. This will not be public.""")
    is_spammer = models.BooleanField(
        default=False,
        help_text="""If they are a spammer, please check this.
        All of their comments will be permanently removed."""
    )

    def __unicode__(self):
        return self.user.username
