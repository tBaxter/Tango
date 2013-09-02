import datetime
import os
import zipfile

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from six import BytesIO

from itertools import chain
from PIL import Image as PIL_Image

from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models import signals

from tango_shared.models import ContentImage
from tango_shared.utils.maptools import get_geocode
from tango_shared.utils.sanetize import sanetize_text

from .signals import update_time

now = datetime.datetime.now()
offset = now - datetime.timedelta(days=5)

UserModel = getattr(settings, "AUTH_USER_MODEL", "auth.User")


REGION_CHOICES = (
    ('Canada', 'Canada'),
    ('Northeast', 'Northeast'),
    ('Southeast', 'Southeast'),
    ('midatlantic', 'Mid-Atlantic'),
    ('Midwest', 'Midwest'),
    ('Central', 'Central'),
    ('Southwest', 'Southwest'),
    ('Rocky', 'Rocky'),
    ('Pacific', 'Pacific'),
    ('Nationwide', 'Nationwide US'),
    ('outside', 'Outside US'),
)


class EventManager(models.Manager):
    """
    Custom manager for the Event model.
    """
    def delete_past_events(self):
        """
        Removes old events. This is provided largely as a convenience for maintenance
        purposes (daily_cleanup). if an Event has passed by more than X days
        as defined by Lapsed and has no related special events it will be deleted
        to free up the event name and remove clutter.
        For best results, set this up to run regularly as a cron job.
        """
        lapsed = datetime.datetime.now() - datetime.timedelta(days=90)
        for event in self.filter(start_date__lte=lapsed, featured=0, recap=''):
            event.delete()


class Event(models.Model):
    submitted_by = models.ForeignKey(
        UserModel,
        limit_choices_to = {'is_active': True},
        related_name="event_submitter"
    )
    name = models.CharField('Event name', max_length=200)
    subhead = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=200, choices=REGION_CHOICES)
    venue = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField("Street Address", max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    website = models.URLField(
        'Event website',
        blank=True,
        null=True,
        help_text="If you have one, make sure it's a complete URL. Don't forget the http://"
    )

    info = models.TextField(
        blank=True,
        null=True,
        help_text="Brief info about the event. Do **not** use HTML, but Markdown is allowed."
    )
    recap = models.TextField(blank=True, null=True, help_text="Post-event recap")
    info_formatted = models.TextField(blank=True, null=True, editable=False)
    recap_formatted = models.TextField(blank=True, null=True, editable=False)


    add_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(help_text="yyyy-mm-dd format")
    end_date = models.DateField(help_text="For multi-day events", blank=True, null=True)

    admin_notes = models.TextField(blank=True, null=True, help_text="Private administrative notes")
    approved = models.BooleanField(default=True)
    geocode = models.CharField(max_length=200, null=True, blank=True, editable=False)
    featured = models.BooleanField(default=False, help_text="Check for featured events")
    has_playlist = models.BooleanField(
        default=True,
        help_text="If checked, playlist submissions will be requested."
    )
    offsite_tickets = models.URLField(
        blank=True,
        null=True,
        help_text="URL to off-site ticket sales"
    )
    ticket_sales_end = models.DateField(blank=True, null=True)
    related_events = models.ManyToManyField(
        "self",
        blank=True,
        related_name="similar_events",
        limit_choices_to = {'featured': True}
    )
    attending = models.ManyToManyField(UserModel, blank=True, null=True, related_name="attendees")

    objects         = EventManager()

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', [self.slug])

    @models.permalink
    def get_gallery_url(self):
        return ('event_slides', [self.slug])

    class Meta:
        ordering = ['-start_date', '-featured']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        geocode = get_geocode(self.city, self.state, self.address, self.zipcode)
        if geocode:
            self.geocode = ', '.join(geocode)
        self.info_formatted = sanetize_text(self.info)
        if self.recap:
            self.recap_formatted = sanetize_text(self.recap)
        super(Event, self).save(*args, **kwargs)

    def ended(self):
        end_date = self.end_date if self.end_date else self.start_date
        if end_date < datetime.date.today():
            return True

    def recently_ended(self):
        """
        Determines if event ended recently (within 5 days).
        Useful for attending list.
        """
        if self.ended():
            end_date = self.end_date if self.end_date else self.start_date
            if end_date >= offset.date():
                return True

    def has_started(self):
        if self.start_date <= datetime.date.today():
            return True

    def comments_open(self):
        return True

    def get_comment_count(self):
        ctype = ContentType.objects.get(app_label__exact="happenings", name__exact='event')
        num_comments = Comment.objects.filter(content_type=ctype.id, object_pk=self.id).count()
        return num_comments

    def get_all_comments(self):
        ctype         = ContentType.objects.get(app_label__exact="happenings", name__exact='event')
        update_ctype  = ContentType.objects.get(app_label__exact="happenings", name__exact='update')
        comments      = Comment.objects.filter(content_type=ctype.id, object_pk=self.id)
        update_ids    = self.update_set.values_list('id', flat=True)
        u_comments    = Comment.objects.filter(content_type=update_ctype.id, object_pk__in=update_ids)
        if self.ended():
            return list(chain(comments, u_comments))
        else:
            return list(chain(comments, u_comments)).reverse()

    def get_all_comments_count(self):
        ctype         = ContentType.objects.get(app_label__exact="happenings", name__exact='event')
        update_ctype  = ContentType.objects.get(app_label__exact="happenings", name__exact='update')
        comments      = Comment.objects.filter(content_type=ctype.id, object_pk=self.id).count()
        update_ids    = self.update_set.values_list('id', flat=True)
        u_comments    = Comment.objects.filter(content_type=update_ctype.id, object_pk__in=update_ids).count()
        count = comments + u_comments
        return count

    def get_all_images(self):
        self_imgs     = self.image_set.all()
        update_ids    = self.update_set.values_list('id', flat=True)
        u_images      = UpdateImage.objects.filter(update__id__in=update_ids)
        return list(chain(self_imgs, u_images))

    def get_all_images_count(self):
        self_imgs     = self.image_set.count()
        update_ids    = self.update_set.values_list('id', flat=True)
        u_images      = UpdateImage.objects.filter(update__id__in=update_ids).count()
        count = self_imgs + u_images
        return count

    def get_top_assets(self):
        images = self.get_all_images()[0:14]
        video  = self.eventvideo_set.all()[0:10]
        return list(chain(images, video))[0:15]

    def get_giveaways(self):
        return self.giveaway_set.filter(closed=False)

    def update_count(self):
        return self.update_set.count()

    def latest_update(self):
        return self.update_set.latest('id')

    def get_latest_updates(self):
        u_count = self.update_count()
        updates = self.update_set.all()
        if u_count == 1:
            return {'count': u_count, 'updates': updates}
        cap = 5
        if self.ended():
            updates = updates.order_by('id')[0:cap]
        else:
            updates = updates.order_by('-id')[0:cap]
        return {'count': u_count, 'updates': updates}

    def get_sidebars(self):
        return self.extrainfo_set.filter(is_sidebar=True)

    def get_extra_pages(self):
        return self.extrainfo_set.filter(is_sidebar=False)


class ExtraInfo(models.Model):
    """
    For sidebar-type additional info on event
    """
    event = models.ForeignKey(Event, verbose_name="Extra info",)
    title = models.CharField(max_length=300)
    slug = models.SlugField(blank=True, help_text="Only needed if this is not a sidebar")
    text = models.TextField()
    text_formatted = models.TextField(blank=True, null=True, editable=False)
    is_sidebar = models.BooleanField(default=False)
    image = models.ImageField(upload_to='img/events/special/', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        self.text_formatted = sanetize_text(self.text)
        super(ExtraInfo, self).save(*args, **kwargs)


class Image(ContentImage):
    """
    Subclasses content image.
    Note we can also have Update Images,
    and Event has a get_all_images() method to combine the two
    """
    event = models.ForeignKey(Event)


class EventVideo(models.Model):
    video = models.ForeignKey('video.Video', related_name="event_video")
    event = models.ForeignKey(Event)


class Schedule(models.Model):
    special_event = models.ForeignKey(Event, related_name='schedule', verbose_name=('Event Schedule'))
    event         = models.CharField("Scheduled Event", max_length=200)
    start         = models.DateTimeField('Start time')
    end           = models.DateTimeField('End time', blank=True, null=True)
    show_time     = models.BooleanField(default=True, help_text="Uncheck to hide time and only show date")
    description   = models.CharField(max_length=400, blank=True, null=True)
    link          = models.CharField(max_length=100, blank=True, null=True)


class Giveaway(models.Model):
    event       = models.ForeignKey(Event, limit_choices_to = {'featured': True})
    question    = models.CharField(max_length=200)
    long_q      = models.TextField("Additional info", blank=True, help_text="If you'd like to clarify or expound. This information will be shown while the giveaway is active.")
    explanation = models.TextField("Answer and/or Explanation", blank=True, help_text="This will be shown when the giveaway is closed")
    pub_time    = models.DateTimeField(auto_now_add=True)
    prize       = models.CharField(max_length=255)
    number      = models.IntegerField(default=1)
    closed      = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.question)

    class Meta:
        ordering = ['-id']
        get_latest_by = "id"

    def get_respondents_list(self):
        return self.giveawayresponse_set.value_list('respondent', flat=True)


class GiveawayResponse(models.Model):
    question   = models.ForeignKey(Giveaway)
    answer     = models.TextField()
    respondent = models.ForeignKey(UserModel, limit_choices_to = {'is_active': True}, editable=False, related_name="giveaway_respondent", blank=True, null=True)
    correct    = models.BooleanField(default=False)
    notes      = models.CharField(blank=True, max_length=255)
    submitted  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.respondent)


class PlaylistItem(models.Model):
    event      = models.ForeignKey(Event)
    user       = models.ForeignKey(UserModel, limit_choices_to = {'is_active': True}, related_name="playlist_submitter")
    title      = models.CharField(max_length=200)
    link       = models.URLField(max_length=200, blank=True, help_text="Optional: Link to a video or tab to help folks learn it.")
    votes      = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        unique_together = (("event", "title"),)


class Update(models.Model):
    """
    Allows updating the event in near real-time, with blog-style content updates.
    """
    event = models.ForeignKey(Event, limit_choices_to = {'featured': True}, db_index=True)
    title = models.CharField("Update title", max_length=200)
    update = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    giveaway = models.ManyToManyField(
        Giveaway,
        null=True,
        blank=True,
        help_text="""Optional. Use this if you want to attach a giveaway to this update.
            Giveaways that aren't attached to an update will be still be attached to the event."""
    )
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserModel, limit_choices_to = {'is_staff': True})
    audio = models.FileField(upload_to='audio/events/special/', blank=True, null=True, help_text="Should be MP3 format")

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('event_update_detail', [str(self.event.slug), str(self.id)])

    def save(self, *args, **kwargs):
        self.update_formatted = sanetize_text(self.update)
        super(Update, self).save(*args, **kwargs)

    def comments_open(self):
        return True

    def get_comment_count(self):
        ctype = ContentType.objects.get(name__exact='update')
        num_comments = Comment.objects.filter(content_type=ctype.id, object_pk=self.id).count()
        return num_comments

    def has_image(self):
        if self.updateimage_set.count():
            return True

    def get_image(self):
        return self.updateimage_set.latest('id')

    def get_top_assets(self):
        return self.updateimage_set.all()

    def get_open_giveaways(self):
        """
        Returns any open giveaways for the :model:`happenings.Update`
        """
        return self.giveaway.filter(closed=False)


class UpdateImage(ContentImage):
    """ Subclasses Content Image to connect images to updates. """
    update  = models.ForeignKey(Update, db_index=True)


class Memory(models.Model):
    """
    Allows users to post their thoughts and memories on an event.
    """
    event = models.ForeignKey(Event, verbose_name="remembered_event", limit_choices_to = {'featured': True})
    author = models.ForeignKey(UserModel)
    thoughts = models.TextField(blank=True)
    thoughts_formatted = models.TextField(blank=True, editable=False)
    photos = models.ManyToManyField(Image, null=True, blank=True, help_text="Optional. Upload some images. Be kind, this isn't Flickr.")
    offsite_photos = models.URLField(null=True, blank=True, help_text="If you've already uploaded photos somewhere else, you can give the gallery URL here.")

    class Meta:
        verbose_name_plural = "memories"

    def __unicode__(self):
        return unicode(self.author)

    @models.permalink
    def get_absolute_url(self):
        return ('memory_detail', [self.event.slug, self.id])

    def save(self, *args, **kwargs):
        self.thoughts_formatted = sanetize_text(self.thoughts_formatted)
        super(Memory, self).save(*args, **kwargs)


class BulkEventImageUpload(models.Model):
    """
    Allows zip file multi-image upload in admin.
    """
    zip_file  = models.FileField(upload_to= "temp/", help_text='Select a .zip file of images to upload.')
    event     = models.ForeignKey(Event)

    def save(self, *args, **kwargs):
        zfile = zipfile.ZipFile(self.zip_file, 'r')
        bad_file = zfile.testzip()
        if bad_file:  # how can we pass this error back to the admin form?
            raise Exception('"{}" in the .zip archive is corrupt.'.format(bad_file))
        # why are we NOT using threading?
        # for a rundown on threading, see: http://www.ibm.com/developerworks/aix/library/au-threadingpython/
        # args are parent, zip file, destination, child
        #t = threading.Thread(target=process_upload, args=[self.event, zfile, "img/events/special/", Image])
        #t.setDaemon(False)
        #t.start()
        this_dir = '{}/{}/'.format(now.year, now.month)  # make sure we have a dir to put these in.
        dir      = "img/events/special/{}".format(this_dir)

        dirpath = settings.MEDIA_ROOT + dir
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        for filename in zfile.namelist():
            # bail if it's not jpg, and skip meta files
            if filename.lower().endswith('.jpg') and not filename.lower().startswith('__'):
                clean_filename = filename.replace('/', '_').lower()
                im = PIL_Image.open(BytesIO(zfile.read(filename)))
                if im.mode not in ('L', 'RGB'):
                    im = im.convert('RGB')
                im.thumbnail((900, 1200))
                temp_handle = BytesIO()
                im.save(temp_handle, 'jpeg')
                temp_handle.seek(0)
                try:
                    img_file = SimpleUploadedFile(clean_filename, temp_handle.read(), 'image/jpeg',)
                except Exception:
                    img_file = None
                if img_file is not None:
                    try:
                        Image.objects.get(image=dir + clean_filename)
                    except Image.DoesNotExist:
                        new_img = Image(
                            event   = self.event,
                            image   = img_file,
                        )
                        new_img.save()
        return  # note that we're not actually saving the zip. No good reason to.


signals.post_save.connect(update_time, sender=Comment)
