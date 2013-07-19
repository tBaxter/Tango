from django import template
from django.conf import settings
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('inclusion/show_video.html')
def show_video(video, top_video=False):
    """
    API-call-free, responsive friendly video embed. Don't forget to use it with the JS that tells Firefox not to use native video, and responsifying CSS.
    """
    return {
        'video': video,
        'MEDIA_URL': settings.MEDIA_URL,
        'top_video': top_video
    }


@register.inclusion_tag('inclusion/old_show_video.html')
def getVideo(video, width='', height=''):
    """
    if video.yt_url:
        Loads a single video from youtube
    if video.ustream_id:
        Loads a single video from ustream
    Be smart and cache results.
    USAGE:
    {% load video_tags %}{% getVideo <video> '' '' %}
    """
    vid_id = 'vidx_' + str(video.id)
    # First we'll look in cache so we can avoid all the API calls
    if cache.get(vid_id):
        data = cache.get(vid_id)
    else:
        if video.yt_url:  # we think it's youtube
            from utils.gdata.youtube import service
            yt_service = service.YouTubeService()
            if video.yt_url.find('&') != -1:
                yt_id = video.yt_url[video.yt_url.find("v=") + 2:video.yt_url.find("&")]
            else:
                yt_id = video.yt_url[video.yt_url.find("v=") + 2:]
            try:
                yt_data = yt_service.GetYouTubeVideoEntry(video_id=yt_id)
            except:
                return
            data = {
                'title': yt_data.media.title.text,
                'description': yt_data.media.description.text,
                'yt_id': yt_id,
                'yt_url': video.yt_url,
                'swf_url': yt_data.GetSwfUrl()
            }
            if video.video_title != data['title']:
                video.video_title = data['title']
                video.save()
        if video.ustream_id:
            # do stuff for ustream
            data = 'ustream'
            # rsplit just in case they put the full url in
            try:
                video = video.ustream_id.rsplit('/')[1]
            except:
                video = video.ustream_id
            height = "800"
            width  = "600"
        else:
            return
        # Now cache it for next time
        cache.set(vid_id, data, 60 * 60)
    return {
        'data': data,
        'height': height,
        'width': width,
        'video': video,
        }
