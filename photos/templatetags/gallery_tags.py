from django import template
from galleries.models import Gallery
from django.conf import settings

register = template.Library()

class GalleryNode(template.Node):
    def __init__(self, num, varname):
        self.varname = varname
        self.num     = num

    def __repr__(self):
        return "<Gallery Node>"

    def render(self, context):
        context[self.varname] = Gallery.objects.all().order_by('-created')[:self.num]
        return ''

class GetGalleries:
    """
    Returns one or more galleries based on num as an object_list.
    Usage:
    {% get_galleries <NUM> as galleries %}
    """
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) != 4:
            raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
        if bits[2] != "as":
            raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
        return GalleryNode(bits[1], bits[3])


register.tag('get_galleries', GetGalleries('get_galleries'))



