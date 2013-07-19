from django import template
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.inclusion_tag('includes/social_links.html')
def social_links(object, user=None, authenticated_request=False, vote_down=False, vote_down_msg=None):
    current_site = Site.objects.get_current()
    c_type = ContentType.objects.get_for_model(object)
    # check if voting available
    voting = False
    if hasattr(object, 'votes'):
        voting = True

    return {
        'object': object,
        'url':    object.get_absolute_url(),
        'site':   current_site,
        'ctype':  c_type,
        'user':   user,
        'voting': voting,
        'vote_down': vote_down,
        'vote_down_msg': vote_down_msg,
        'authenticated_request': authenticated_request,
    }
