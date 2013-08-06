from django import template
from django.conf import settings

from photos.models import Gallery

register = template.Library()


@register.assignment_tag()
def get_galleries(count=5):
    """
    Returns one or more galleries based on num as an object_list.
    Usage:
    {% get_galleries <NUM> as galleries %}
    """
    return Gallery.published.all()[:count]


@register.inclusion_tag('galleries/includes/related_galleries.html')
def get_related_galleries(gallery, count=5):
    """
    Gets latest related galleries from same section as originating gallery.

    Count defaults to five but can be overridden.

    Usage: {% get_related_galleries gallery <10> %}
    """
    # just get the first cat. If they assigned to more than one, tough
    try:
        cat = gallery.sections.all()[0]
        related = cat.gallery_categories.filter(published=True).exclude(id=gallery.id).order_by('-id')[:count]
    except:
        related = None
    return {'related': related, 'MEDIA_URL': settings.MEDIA_URL}
