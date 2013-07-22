from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import truncatewords

UserModel = getattr(settings, "AUTH_USER_MODEL", "auth.User")


EMAIL_CHOICES = (
    ('1', 'Send to all recipients'),
    ('2', 'Create selectable list of recipients'),
)


class Recipient(models.Model):
    """
    A recipient is a pre-defined person who can be selected from a list to receive messages.
    Their email will not be exposed, so you must define both name and email address.
    """
    name   = models.CharField('Recipient', max_length=200)
    email  = models.EmailField('Routes to', max_length=200)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '%s: %s' % (self.name, self.email)

    def found_on_form(self):
        """
        Helper method to show which forms this user is being used on.
        """
        return ','.join(self.contactform_set.values_list('name', flat=True))


class ContactFormController(models.Model):
    """
    Defines the available options to build the desired contact form.
    """
    name = models.CharField(
        max_length=200,
        help_text="A name for this contact form. Can simply be 'contact us'"
    )
    slug = models.CharField(
        max_length=200,
        help_text="A unique identifier for this form used for the URL. Should prepopulate."
    )
    recipients = models.ManyToManyField(
        UserModel,
        limit_choices_to={'is_staff': True},
        blank=True,
        null=True,
        help_text="Select staffers the form should be emailed to. Optional.",
        verbose_name='Staff recipients'
    )
    other_recipients = models.ManyToManyField(
        Recipient,
        blank=True,
        null=True,
        help_text="""
            If you want a recipient who isn't in the staff list,
            provide the info here.
            """
    )
    send_emails = models.BooleanField(
        default=True,
        help_text="Uncheck if contacts should be stored to the database only."
    )
    store_in_db = models.BooleanField(
        default=False,
        help_text="""
            Check if you would like the form stored to the database.
            Note: If you select 'Store in database' no e-mail will be sent.
            The messages will be stored for later review.
            """
    )
    email_options = models.CharField(
        max_length=1,
        choices=EMAIL_CHOICES,
        help_text="""
            Select whether contacts be automatically emailed to all recipients,
            or if the user should see a selectable list to choose from.
            """
    )
    request_contact_info = models.BooleanField(
        default=False,
        help_text="""
            Check if you require the sender's address and phone.
            Remember, this is intrusive and kind of jerky.
            """
    )
    allow_uploads = models.BooleanField(
        default=False,
        help_text="Check if you will allow photo uploads with contacts."
    )
    thank_you = models.TextField(
        blank=True,
        help_text="Custom thank you message. Optional."
    )
    pre_form_msg = models.TextField(
        "Introductory message",
        blank=True,
        help_text="""
            If you would like a custom message before the form, please give it here.
            Optional. And remember, people know how to fill out a contact form. Just get to the point.
            """
    )
    limit_words = models.IntegerField(
        blank=True,
        null=True,
        help_text="""
            If you would like to limit the response length,
            please give the maximum number of words allowed. Example: 200.
            """
    )
    site = models.ForeignKey(
        Site,
        blank=True,
        null=True
    )
    require_auth = models.BooleanField(
        "Require sign-in",
        default=False,
        help_text="If checked, the form can only be submitted by authenticated, signed-in visitors."
    )
    ask_for_subject = models.BooleanField(
        default=True,
        help_text="If unchecked, the form will have no subject line at all."
    )
    override_subject = models.CharField(
        "Subject Line",
        max_length=150,
        blank=True,
        null=True,
        help_text="""
            Provides a default subject for submission emails.
            If left blank, the submitter can write their own.
            """)
    subject_label = models.CharField(
        blank=True,
        max_length=150,
        null=True,
        help_text="""
            Allows for customizing the subject field label. By default, it is "Subject".
            If you would like the label to read something else, such as "Title", enter it here.
            Note: if you have overridden subject, the subject is not shown, and needs no subject label.
            """)
    body_label = models.CharField(
        blank=True,
        max_length=150,
        null=True,
        help_text="""
            Allows for customizing the body field label.
            By default, it is "Your message".
            If you would like the label to be something else, such as "Body", enter it here.
            """
    )

    class Meta:
        verbose_name = "contact form controller"

    def __unicode__(self):
        return "%s" % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('contact_form_builder', [self.slug])


class Contact(models.Model):
    """
    The received message from the form.
    """
    controller = models.ForeignKey(ContactFormController)
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField(max_length=200)
    subject = models.CharField(
        max_length=200,
        blank=True
    )
    body = models.TextField()
    photo = models.ImageField(
        upload_to='img/contact',
        blank=True,
        null=True
    )
    submitted = models.DateField(auto_now_add=True)
    publish = models.BooleanField('Published', default=False)
    send_a_copy = models.BooleanField(
        default=False,
        help_text="Send me a copy of my e-mail"
    )
    user = models.ForeignKey(
        UserModel,
        editable=False,
        blank=True,
        null=True,
        help_text="In some cases, we may require submission from an authenticated user"
    )
    site = models.ForeignKey(Site, default=settings.SITE_ID)
    # if request_contact_info is True
    contact_address = models.TextField(
        blank=True,
        help_text="For verification, not publication.")
    contact_city = models.TextField("City", blank=True)
    contact_state = models.CharField(
        "State/Province",
        max_length=2,
        blank=True
    )
    contact_phone = models.CharField(
        "Phone",
        max_length=12,
        blank=True,
        help_text="For verification, not publication."
    )

    class Meta:
        verbose_name = "submitted content"
        verbose_name_plural = "submitted content"

    def __unicode__(self):
        return "%s" % (self.subject)

    @models.permalink
    def get_absolute_url(self):
        return ('contact_detail', [str(self.id)])

    def is_from_site(self):
        return settings.SITE_ID == self.site.id

    def has_photo(self):
        return hasattr(self, 'photo')
    has_photo.boolean = True

    def summary(self):
        return truncatewords(self.body, 60)
