import django.conf.global_settings as DEFAULT_SETTINGS

### Tango-unique settings

# Thumbnail aliases determines default image sizes for easy-thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'thumb':  {'size': (50, 50),   'autocrop': True, 'crop': 'smart', 'upscale': True},
        't_80':   {'size': (80, 80),   'autocrop': True, 'crop': 'smart', 'upscale': True},
        't_180':  {'size': (180, 180), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        't_180t': {'size': (180, 240), 'autocrop': True, 'crop': '0,-10', 'upscale': True},
        't_180u': {'size': (180, 240), 'autocrop': True},
        't_360':  {'size': (360, 360), 'autocrop': True, 'crop': 'smart', 'upscale': True},
        't_360u': {'size': (360, 540), 'autocrop': True},
        't_420':  {'size': (420, 420), 'autocrop': True, 'crop': 'scale'},
        't_540':  {'size': (540, 540), 'autocrop': True, 'crop': 'scale'},
        't_640':  {'size': (640, 640), 'autocrop': True, 'crop': 'scale'},
        't_720':  {'size': (720, 720), 'autocrop': True, 'crop': 'scale'},
        't_960':  {'size': (960, 960), 'autocrop': True, 'crop': 'scale'},
    },
}

# sets default pagination
PAGINATE_BY = 25

# Google analytics GA code
GOOGLE_ANALYTICS_ID = ''

# Project name
PROJECT_NAME = 'tango'

# if set to false, RESTRICT_CONTENT_TO_SITE will allow
# sites/projects to share content.
# If true, content will be limited to the current site.
RESTRICT_CONTENT_TO_SITE = True

# If set to true, additional fields news organizations
# need will be added, including options to mark content as
# opinion/editorial, dateline, and noting another source as
# the origin of the content.
NEWS_SOURCE = True

# Comment moderation settings
# Number of days after publication until comments close:
COMMENTS_CLOSE_AFTER = 30
# Number of days after publication until comments require moderation:
COMMENTS_MOD_AFTER = 15


# tango apps will be added to installed apps. Or should be.
TANGO_APPS = (
    'tango_capo',
    'tango_shared',
    'articles',
    'autotagger',
    'contact_manager',
    'happenings',
    'photos',
    'user_profiles',
    'video',
    'typogrify',
    'voting',
    'easy_thumbnails',
)


### Django settings...

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Adds Context processors you'll want.
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'tango_shared.context_processors.site_processor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
