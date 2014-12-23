SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

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
