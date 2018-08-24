from urllib.parse import parse_qs, urlsplit
from urllib.request import urlopen 

from django.template.defaultfilters import slugify

import untangle

#xml_media = xmltramp.Namespace('http://search.yahoo.com/mrss/')


def get_youtube_data(video):
    """
    Helper to extract video and thumbnail from youtube
    """
    video.source = 'youtube'
    if 'youtube.com/watch' in video.url:
        parsed = urlsplit(video.url)
        query  = parse_qs(parsed.query)
        try:
            video.key  = query.get('v')[0]
        except IndexError:
            video.key = None
    else:
        video.key = video.url.rsplit('/', 1)[1]
    video.embed_src = 'http://www.youtube.com/embed/'

    # api docs
    #          http://gdata.youtube.com/feeds/api/videos/hNRHHRjep3E
    # https://www.googleapis.com/youtube/v3/videos?id=hNRHHRjep3E&part=snippet,contentDetails,statistics
    api_url = 'http://gdata.youtube.com/feeds/api/videos/{}'.format(video.key)
    video_data = urlopen(api_url).read()
    xml = untangle.parse(video_data)

    video.title = xml.title
    video.slug = slugify(video.title)
    video.summary = xml.content
    #video.thumb_url = xml[xml_media.group][xml_media.thumbnail:][1]('url')
    return video


def get_vimeo_data(video):
    """
    Helper to extract video and thumbnail from vimeo.
    """
    #http://vimeo.com/67325705 -- Tumbleweed Tango
    video.source = 'vimeo'
    video.key = video.url.rsplit('/', 1)[1]
    video.embed_src = 'http://player.vimeo.com/video/'

    api_url = 'http://vimeo.com/api/v2/video/{}.xml'.format(video.key)
    #video_data = urlopen(api_url).read()
    xml = untangle.parse(api_url)
    xmlvideo = xml.videos.video
    video.title = xmlvideo.title.cdata
    video.slug = slugify(video.title)
    video.summary = xmlvideo.description.cdata
    video.thumb_url = xmlvideo.thumbnail_large.cdata
    return video


def get_ustream_data(video):
    """
    Helper to extract video and thumbnail from ustream.
    """

    video.source = 'ustream'
    video.key = video.url.rsplit('/', 1)[1]
    video.embed_src = 'http://www.ustream.tv/embed/'
    if 'recorded' in video.url:
        video.embed_src += '/recorded/'
    video.title = "Ustream video"
    video.slug = 'ustream-{}'.format(video.key)
    return video
