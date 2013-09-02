import urllib

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from django.template.defaultfilters import slugify

from tango_shared.utils import xmltramp

xml_media = xmltramp.Namespace('http://search.yahoo.com/mrss/')


def get_youtube_data(video):
    """
    Helper to extract video and thumbnail from youtube
    """
    video.source = 'youtube'
    if 'youtube.com/watch' in video.url:
        parsed = urlparse.urlsplit(video.url)
        query  = urlparse.parse_qs(parsed.query)
        try:
            video.key  = query.get('v')[0]
        except IndexError:
            video.key = None
    else:
        video.key = video.url.rsplit('/', 1)[1]
    video.embed_src = 'http://www.youtube.com/embed/'
    #http://gdata.youtube.com/feeds/api/videos/Agdvt9M3NJA
    api_url = 'http://gdata.youtube.com/feeds/api/videos/{}'.format(video.key)
    video_data = urllib.urlopen(api_url).read()
    xml = xmltramp.parse(video_data)

    video.title = unicode(xml.title)
    video.slug = slugify(video.title)
    video.summary = unicode(xml.content)
    video.thumb_url = xml[xml_media.group][xml_media.thumbnail:][1]('url')
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
    video_data = urllib.urlopen(api_url).read()
    xml = xmltramp.parse(video_data)
    video.title = unicode(xml.video.title)
    video.slug = slugify(video.title)
    video.summary = unicode(xml.video.description)
    video.thumb_url = unicode(xml.video.thumbnail_large)
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
