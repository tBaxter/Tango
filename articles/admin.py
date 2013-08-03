from django.contrib import admin

from .models import ArticleImage, Sidebar, Destination, Category, Brief, Article
from .models import supports_video, supports_polls

from tango_admin.admin import TextCounterWidget

if supports_video:
    from video.admin import VideoInline


class ArticleImagesInline(admin.TabularInline):
    model = ArticleImage
    extra = 3


class SidebarInline(admin.TabularInline):
    model = Sidebar
    extra = 2


class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/admin/inline_reorder.js',)

    ordering = ['-created']
    list_display = ('title', 'author', 'destination', 'created',)
    list_filter = ('created', 'last_modified', 'enable_comments', 'publication', 'destination')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['body', 'title']
    filter_horizontal = ('sections', 'articles', 'galleries')
    inlines = [
        ArticleImagesInline,
        SidebarInline,
    ]
    if supports_video:
        inlines.append(VideoInline)
    """
    if NEWS_SITE:
        opinion         = models.BooleanField("Opinion/Editorial", default=False)
        source          = models.CharField(max_length=200, default=SOURCE, blank=True, null=True)
        dateline        = models.CharField(max_length=200, blank=True, null=True)
    """
    related = ('Related', {
        'fields': ['galleries', 'articles'],
        'description': 'Other content directly related to this article'
    })
    if supports_polls:
        related[1]['fields'].insert(0, 'polls')

    fieldsets = (
        ('Routing', {'fields': ('destination', 'sections')}),
        ('Author info', {'fields': (('author', 'guest_author'))}),
        ('Header', {'fields': ('overline', 'title', 'subhead')}),
        ('Content', {'fields': ('summary', 'body', 'pull_quote', 'endnote')}),
        ('Admin fields', {
            'description': 'You should rarely, if ever, need to touch these fields.',
            'fields': ('slug', 'enable_comments', 'sites', 'override_url'),
            'classes': ['collapse']
        }),
        related,
        ('Meta',     {
            'fields': (('publication'), 'featured'),
            'description': 'Additional information about this story'
        }),
    )


class BriefAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'text')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            kwargs['widget'] = TextCounterWidget()
        return super(BriefAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(Destination)
admin.site.register(Category)
admin.site.register(Brief, BriefAdmin)
admin.site.register(Article, ArticleAdmin)
