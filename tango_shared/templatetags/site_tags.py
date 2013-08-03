import datetime
from itertools import chain

from django import template
from django.utils.timesince import timesince

from articles.models import Article
from photos.models import Gallery
from video.models import Video

register = template.Library()


@register.inclusion_tag('includes/formatted_time.html')
def format_time(date_obj, time_obj=None, datebox=False, dt_type=None):
    """
    Returns formatted HTML5 elements based on given datetime object.
    By default returns a time element, but will return a .datebox if requested.

    dt_type allows passing dt_start or dt_end for hcal formatting.
    link allows passing a url to the datebox.

    Usage:
    {% format_time obj.pub_date %}
    {% format_time obj.start_date 'datebox' 'dtstart' %}
    {% format_time obj.end_date obj.end_time 'datebox' 'dt_end' %}
    """
    if not time_obj:
        try:
            time_obj = date_obj.time
        except:
            time_obj = None
    return {
        'date_obj': date_obj,
        'time_obj': time_obj,
        'datebox': datebox,
        'current_year': datetime.date.today().year,
        'dt_type': dt_type,
    }


@register.filter
def short_timesince(date):
    """
    A shorter version of Django's built-in timesince filter.
    Selects only the first part of the returned string,
    splitting on the comma.

    Falls back on default Django timesince if it fails.

    Example: 3 days, 20 hours becomes "3 days".

    """
    try:
        return timesince(date).split(", ")[0]
    except IndexError():
        timesince(date)


@register.filter
def fix_indents(value):
    """
    Strips tabs and extra spaces from user-submitted text
    to avoid triggering pre code in markdown.

    Use this with caution.
    It's much better to sanitize the content before save().

    Likely to be replaced by a smarter minification.
    """
    value = value.replace('\t', '').replace('    ', ' ')
    return value


@register.inclusion_tag('includes/fresh_content.html')
def get_fresh_content(top=4, additional=10, featured=False):
    """
    Returns published *Featured* content (articles, galleries, video, etc)
    and an additional batch of fresh regular (featured or not) content.
    The number of objects returned is defined when the tag is called.
    The top item type is defined in the sites admin for sites that
    have the supersites app enabled.
    If "featured" is True, will limit to only featured content.
    Usage:
        {% get_fresh_content 5 10 %}
        Would return five top objects and 10 additional
        {% get_fresh_content 4 8 featured %}
        Would return four top objects and 8 additional, limited to featured content.
    What you get:
        'top_item':       the top featured item
        'top_item_type':  the content type for the top item (article, gallery, video)
        'featured':       Additional featured items. If you asked for 5 featureed items, there will be 4
                          (five - the one that's in top item)
        'articles':       featured articles, minus the top item
        'galleries':      featured galleries, minus the top item
        'vids':           featured video, minus the top item,
        'more_articles':  A stack of articles, excluding what's in featured, sliced to the number passed for <num_regular>,
        'more_galleries': A stack of galleries, excluding what's in featured, sliced to the number passed for <num_regular>,
        'additional':     A mixed list of articles and galleries, excluding what's in featured, sliced to the number passed for <num_regular>,
    """
    articles = Article.published.only('title', 'summary', 'slug', 'created')
    galleries = Gallery.published.only('title', 'summary', 'slug', 'created')
    videos = Video.published.only('title', 'summary', 'slug', 'created')

    if featured:
        articles = articles.filter(featured=True)
        galleries = galleries.filter(featured=True)
        videos = videos.filter(featured=True)

    # now slice to maximum possible for each group
    # and go ahead and make them lists for chaining
    max_total = top + additional
    articles = list(articles[:max_total])
    galleries = list(galleries[:max_total])
    videos = list(videos[:max_total])

    # chain the lists now
    content = chain(articles, galleries, videos)
    content = sorted(content, key=lambda instance: instance.created)
    content.reverse()

    top_content = content[:top]
    additional_content = content[top:max_total]
    return {
        'top_content': top_content,
        'additional_content': additional_content,
    }
