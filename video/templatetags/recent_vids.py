from django import template
from video.models import Video
from django.conf import settings

register = template.Library()

class VideoNode(template.Node):
    def __init__(self,varname):
        self.varname = varname

    def __repr__(self):
        return "<Video Node>"

    def render(self, context):
        context[self.varname] = Video.objects.filter(site=settings.SITE_ID).order_by('-id')[:3]
        return ''

class GetVideoList:
    """
    {% get_video_list as video_list %}
    """
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        bits = token.contents.split()
        if len(bits) != 3:
            raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
        if bits[1] != "as":
            raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
        return VideoNode(bits[2])


register.tag('get_video_list', GetVideoList('get_video_list'))

