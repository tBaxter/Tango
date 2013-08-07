from django import template

from video.models import Video

register = template.Library()


@register.assignment_tag()
def get_video_list(count=5):
    """
    Returns recent videos limited to count.
    Usage: "{% get_video_list as video_list %}"
    """
    return Video.published.all()[:count]


@register.inclusion_tag('video/includes/show_video.html')
def show_video(video, top_video=False):
    """
    API-call-free, responsive friendly video embed. Don't forget to use it with the JS that tells Firefox not to use native video, and responsifying CSS.
    """
    return {
        'video': video,
        'top_video': top_video
    }
