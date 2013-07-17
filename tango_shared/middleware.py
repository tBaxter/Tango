import re
from django.utils.html import strip_spaces_between_tags as strip_spaces

RE_MULTISPACE = re.compile(r"\s{2,}")
RE_NEWLINE = re.compile(r"\n")


class SpacelessMiddleware(object):
    """
    Removes spaces between tags site-wide.
    Deprecated by smarter MinifyHTMLMiddleware below.
    """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = strip_spaces(response.content)
        return response


class MinifyHTMLMiddleware(object):
    """ Remove newlines and extraneous spaces from HTML output """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_NEWLINE.sub("", response.content)
        return response
