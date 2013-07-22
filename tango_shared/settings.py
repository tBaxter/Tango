import django.conf.global_settings as DEFAULT_SETTINGS

# sets default pagination
PAGINATE_BY = 25

# Google analytics GA code
GOOGLE_ANALYTICS_ID = ''

# The Project name. If this is set in your settings, remove it.
PROJECT_NAME = 'tango'

TANGO_APPS = (
              #'tango_admin',
    'tango_capo',
    'tango_shared',
    'articles',
    'autotagger',
    'contact_manager',
    'galleries',
    'happenings',
    'tango_capo',
    'user_profiles',
    'video',
    'typogrify',
    'voting',
)

# Adds Context processors you'll want.
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'tango_shared.context_processors.site_processor',
)
