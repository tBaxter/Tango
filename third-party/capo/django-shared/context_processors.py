import datetime

from django.conf import settings
from django.contrib.sites.models import Site


def site_processor(request):
    """
    Passes some handy variables over to base_all.html and other templates.
    Be sure to set the settings if you want to use them.
    """
    return {
      'site'           : Site.objects.get_current(),
      'year'           : datetime.datetime.now().year,
      'ga_code'        : settings.GOOGLE_ANLYTICS_ID,
      'project_name'   : settings.PROJECT_NAME,
    }
