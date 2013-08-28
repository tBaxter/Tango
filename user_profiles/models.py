import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.html import strip_tags

from tango_shared.models import set_img_path
from tango_shared.utils.sanetize import sanetize_text
from tango_shared.utils.maptools import get_geocode

THEME_CHOICES = [(theme, theme.capitalize()) for theme in getattr(settings, 'ALLOWABLE_THEMES', [])]


class Profile(AbstractUser):
    """
    Subclasses AbstractUser to provide site-specific user fields.
    """
    display_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="""
        If you would prefer a different screen name, enter it here.
        Spaces are allowed. Note: your username will not change.
        """
    )
    street_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Will never be shown publicly on the site.")
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(
        'ZIP/Postal Code',
        max_length=10,
        blank=True,
        help_text="Will never be shown publicly on the site."
    )
    interests = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(blank=True, null=True)
    homepage = models.URLField('Your web site', blank=True)
    bio = models.TextField(help_text='Tell us a bit about yourself.', blank=True, null=True)
    bio_formatted = models.TextField(blank=True, editable=False)
    signature = models.CharField(
        max_length=255,
        blank=True,
        help_text="""
            You can have a short signature line on the posts and comments.
            Members who choose to view signatures can see it. HTML is not allowed.
            """
    )
    geocode = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=set_img_path)
    if 'fretboard' in settings.INSTALLED_APPS:
        post_count = models.IntegerField(default="0", editable=False)

    #preferences
    display_on_map = models.BooleanField(default=True)
    open_links = models.BooleanField(
        "Open links in new window",
        default=False,
        help_text="Check if you would like links to automatically open in a new window."
    )
    show_signatures = models.BooleanField(
        default=False,
        help_text="Check if you would like to see signatures attached to forum posts."
    )
    theme = models.CharField(max_length=100, blank=True, choices=THEME_CHOICES)

    class Meta:
        ordering = ('display_name',)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        needs_geocode = False
        if self.id is None:  # For new user, only set a few things:
            self.display_name = self.get_display_name()
            needs_geocode = True
        else:
            old_self = self.__class__.objects.get(id = self.id)
            if old_self.city != self.city or old_self.state != self.state or self.geocode is None:
                needs_geocode = True
            if old_self.display_name != self.display_name or old_self.first_name != self.first_name or old_self.last_name != self.last_name:
                self.display_name = self.get_display_name()  # check if display name has changed
            if old_self.avatar and old_self.avatar != self.avatar:
                os.remove(old_self.avatar.path)
        if self.city and self.state and needs_geocode:
            geocode = get_geocode(self.city, self.state, street_address=self.street_address, zipcode=self.zip)
            if geocode and geocode != '620':
                self.geocode = ', '.join(geocode)
        if self.signature:
            self.signature = strip_tags(self.signature)
        if self.bio:
            self.bio_formatted = sanetize_text(self.bio)

        super(Profile, self).save(*args, **kwargs)

    # fix this for current URL -- use permalink
    def get_absolute_url(self):
        return reverse('view_profile', args=[self.username])

    def get_display_name(self):
        """
        Determined display screen name based on the first of
        display_name, full name, or username.
        """
        if self.display_name:
            return self.display_name
        elif self.first_name and self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name)
        else:
            return self.username
