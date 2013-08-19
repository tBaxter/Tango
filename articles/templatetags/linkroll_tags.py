from django import template
from articles.models import LinkRoll, Link

register = template.Library()


@register.inclusion_tag('articles/includes/linkroll_list.html')
def get_linkrolls(num='All', destination_slug=None, *args, **kwargs):
    """
    Takes an optional number and destination slug and returns a list of LinkRolls.
    Given a number, return list limited to the given number.
    Given a destination slug, limit linkrolls to the matching destination.
    Usage:
        {% get_linkrolls %}
        {% get_linkrolls 5 %}
        {% get_linkrolls 5 some_slug %}
    """
    if destination_slug:
        linkrolls = LinkRoll.objects.filter(destination__slug=destination_slug)
    else:
        linkrolls = LinkRoll.objects.all()

    if num is not 'All':
        linkrolls = linkrolls[0:num]

    return {
        'object_list': linkrolls
    }


@register.inclusion_tag('articles/includes/linkroll_detail.html')
def get_linkroll_details(destination_slug, num='All', *args, **kwargs):
    """
    Takes an optional number and destination (by id) and returns a list of links for the given linkroll.
    Given a number, return list limited to the given number.
    Given a destination slug, limit linkrolls to the matching destination.
    Usage:
        {% get_linkroll_details some_slug %}
        {% get_linkroll_details some_slug 5 %}
    """
    links = Link.objects.filter(destination__slug=destination_slug)
    if num:
        links = links[0:num]

    return {
        'link_list': links
    }
