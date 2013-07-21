import datetime

from django.conf import settings
from django.contrib.sites.models import Site

now = datetime.datetime.now()
one_day_ago = now - datetime.timedelta(days=1)

ALLOWABLE_THEMES = getattr(settings, 'ALLOWABLE_THEMES', None)


def site_processor(request):
    authenticated_request = request.user.is_authenticated()
    theme = request.COOKIES.get('theme', None)
    if not theme:
        theme = getattr(request.user, "theme", None)
    if not theme or theme not in ALLOWABLE_THEMES:
        theme = getattr(settings, 'DEFAULT_THEME', None)

    last_seen = request.session.get('last_seen', now)
    last_seen_fuzzy = last_seen
    if last_seen > one_day_ago:
        last_seen_fuzzy = one_day_ago

    return {
        'site'            : Site.objects.get_current(),
        'now'             : now,
        'year'            : now.year,
        'ga_code'         : settings.GOOGLE_ANALYTICS_ID,
        'project_name'    : settings.PROJECT_NAME,
        'current_path'    : request.get_full_path(),
        'last_seen'       : last_seen,
        'last_seen_fuzzy' : last_seen_fuzzy,
        'theme'           : theme,
        'authenticated_request': authenticated_request,
    }
