import datetime
from itertools import chain

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import truncatewords

from .managers import DestinationManager, BlogManager, ArticlesManager, PublishedArticlesManager
from .signals import auto_tweet

from autotagger.autotag_content import autotag
from tango_shared.models import ContentImage


########## CONFIG ###########
supports_video = False
if 'video' in settings.INSTALLED_APPS:
    from video.models import Video
    supports_video = True

supports_polls = False
if 'polls' in settings.INSTALLED_APPS:
    from polls.models import Poll
    supports_polls = True

# Comment moderation settings
closing    = getattr(settings, 'COMMENTS_CLOSE_AFTER', 30)
moderating = getattr(settings, 'COMMENTS_MOD_AFTER', 30)


# possibly to do.. add "news" config with source, opinion, etc.

PUBLICATION_CHOICES = (
    ('Draft', 'Draft'),
    ('Proofed', 'Proofed'),
    ('Published', 'Published'),
)
now = datetime.datetime.now()
offset = datetime.date.today() - datetime.timedelta(days=90)

UserModel = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# News site settings.
NEWS_SITE = False
SOURCE      = getattr(settings, 'SOURCE', '')


########## END CONFIG ###########


class Assignment(models.Model):
    """
    Defines destinations an article may be assigned to
    and allow for routing to the correct destination.

    Destination assignments can be blogs, article groups, etc.

    To-do: add site(s)
    """
    title   = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    slug    = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    author  = models.ForeignKey(UserModel, limit_choices_to = {'is_active': True, 'groups__name': 'Blogger'}, blank=True, null=True)
    icon    = models.ImageField(upload_to="img/content/icons/", blank=True, help_text="If this is not a personal blog, please provide a representative image")
    active  = models.BooleanField(default=True)
    is_blog = models.BooleanField(default=True)

    objects = DestinationManager()
    blogs   = BlogManager()

    class Meta:
        verbose_name = "destination"
        verbose_name_plural = "destinations"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.is_blog:
            return '/blogs/' + self.slug
        return '/' + self.slug

    def get_feed_url(self):
        return '/feeds' + self.get_absolute_url()


class Category(models.Model):
    """
    Allows for content categorization.
    """
    category = models.CharField(max_length=200)
    slug     = models.SlugField(max_length=200)
    summary  = models.TextField(blank=True)
    image    = models.ImageField(upload_to="img/content/cats", blank=True)
    blog_cat = models.BooleanField(default=False, help_text="Only allow (and show) this category on blogs.")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['category']

    def __unicode__(self):
        return self.category


class Article(models.Model):
    author          = models.ForeignKey(UserModel, limit_choices_to={'is_staff': True}, blank=True, null=True)
    guest_author    = models.CharField(max_length=200, blank=True, help_text="If the author is not on staff or in the system.")
    kicker          = models.CharField(max_length=200, blank=True, help_text="A short headline over the main headline.")
    title           = models.CharField('Headline', max_length=200, help_text="The title for this content.")
    subhead         = models.CharField('Deck', max_length=200, blank=True, help_text="A short extra headline below the main headline.")
    slug            = models.SlugField(max_length=200)
    summary         = models.TextField(blank=True, help_text="You should summarize the content. It's better for search engines, and for people browsing lists of content. If you don't, a summary will be created. But you should.")
    body            = models.TextField()
    pull_quote      = models.TextField(blank=True)
    endnote         = models.TextField(blank=True, null=True, help_text="A short note after the body.")
    featured        = models.BooleanField(default=False)

    enable_comments = models.BooleanField(default=True)
    publication     = models.CharField(max_length=32, choices=PUBLICATION_CHOICES, default='Published')
    sites           = models.ManyToManyField(Site, default=[settings.SITE_ID, ], blank=False, null=True)
    override_url    = models.URLField(blank=True, help_text="Direct link to story elsewhere.")

    destination     = models.ForeignKey(Assignment)
    sections        = models.ManyToManyField(Category, blank=True, null=True)

    # RELATED
    galleries       = models.ManyToManyField('galleries.Gallery', related_name="article_galleries", blank=True)
    articles        = models.ManyToManyField('self', related_name="related_articles", blank=True, null=True, limit_choices_to={'publication': 'Published'})

    created         = models.DateTimeField(auto_now_add=True)
    last_modified   = models.DateTimeField(auto_now=True)

    if NEWS_SITE:
        opinion  = models.BooleanField("Opinion/Editorial", default=False)
        source   = models.CharField(max_length=200, default=SOURCE, blank=True, null=True)
        dateline = models.CharField(max_length=200, blank=True, null=True)

    if supports_video:
        videos = generic.GenericRelation(Video)

    if supports_polls:
        polls = models.ManyToManyField(Poll, blank=True, null=True)

    # Managers
    objects   = ArticlesManager()
    published = PublishedArticlesManager()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.override_url:
            return self.override_url
        if self.destination.is_blog:
            return ('blog_entry_detail', [self.destination.slug, self.slug])
        return ('article_detail', [self.slug])

    def save(self, *args, **kwargs):
        if not self.summary:
            self.summary = truncatewords(self.body, 50)
        super(Article, self).save()

    def get_top_assets(self):
        """
        Returns chained list of top assets (photos and video) for commonized templates.
        """
        imgs = self.articleimage_set.all()
        vids = self.videos.all()
        return list(chain(imgs, vids))

    def get_image(self):
        try:
            return self.articleimage_set.all()[0].image
        except IndexError:
            return None

    def autotag_body(self):
        """
        Auto-inserts links for matching content and establishes M2M relationshiops.
        See utils.autotag_content import autotag for details.
        """
        return autotag(self, self.body)

    def get_comment_count(self):
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.comments.models import Comment
        ctype = ContentType.objects.get(name__exact='article')
        num_comments = Comment.objects.filter(content_type=ctype.id, object_pk=self.id).count()
        return num_comments

    def comments_open(self):
        close_date = (self.created + datetime.timedelta(days=closing))
        if close_date > now:
            return True


class Sidebar(models.Model):
    # make sidebars separate content or not. see happenings.
    article   = models.ForeignKey(Article, related_name="related_sidebars")
    headline  = models.CharField(max_length=200, blank=True)
    body      = models.TextField()


class Brief(models.Model):
    text     = models.TextField(help_text="Limit yourself to 140 characters for Twitter integration")
    pub_date = models.DateTimeField(auto_now_add=True)
    link     = models.CharField(max_length=200, blank=True, null=True, help_text="Use full URL, with http://")
    sites    = models.ManyToManyField(Site)
    tweet    = models.BooleanField("Send to Twitter", default=False)

    def __unicode__(self):
        return unicode(self.pub_date)

    @models.permalink
    def get_absolute_url(self):
        return ('brief_detail', [self.id])


class ArticleImage(ContentImage):
    article  = models.ForeignKey(Article)


class SidebarImage(ContentImage):
    sidebar  = models.ForeignKey(Sidebar)

models.signals.post_save.connect(auto_tweet, sender=Brief)
