import os

ROOT = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(ROOT, '..', '%s-data' % os.path.basename(ROOT)))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ['test@example.com']
MANAGERS = ADMINS

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(DATA_ROOT, 'site.db'),
#         # 'ENGINE': 'django.db.backends.mysql',
#         # 'HOST': 'localhost',
#         #		'NAME': 'snackpref',
#         'USER': 'snackpref',
#         'PASSWORD': 'snackpref',
#     }
# }


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(DATA_ROOT, 'site.db'),
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'dpt',
        'USER': 'root',
        'PASSWORD': '',
        # 'PASSWORD': 'd2TEJG4q',
    }
}

TIME_ZONE = 'UTC'
DATETIME_FORMAT = 'd/m/Y H:i:s'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
STATIC_ROOT = ROOT + '/static'
STATIC_URL = '/static/'
DROPBOX_ROOT = '/home/yummysnack/snackpref-data/40 Meals & Restaurant Logos'
ADMIN_MEDIA_PREFIX = '/admin/media/'
#STATICFILES_DIRS = (os.path.join(ROOT, 'static'),)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',  # 'django.core.context_processors.auth',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',  # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'disable_csrf.disableCSRF',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'html'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'registration',
    'app',
)

ACCOUNT_ACTIVATION_DAYS = 666
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'