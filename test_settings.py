SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sites',
    'tango_shared',
    'tango_user',
    'video',
    'typogrify', # installed by shared, keeps templates happy
    'voting',
    'easy_thumbnails'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

AUTH_USER_MODEL = 'tango_user.Profile'
ROOT_URLCONF = 'test_urls'

#stripped down middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ACTIVITY_MONITOR_MODELS = (
    {
        'model': 'auth.user',     # Required: the model to watch.
        'verb': " joined ",
    },
)
