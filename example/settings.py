import os
import metasettings

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

METASETTINGS_METHOD = metasettings.HOSTNAME
METASETTINGS_DIR = PROJECT_PATH + '/settings'
METASETTINGS_PATTERNS = (
	(r'production1', 'production'),
	(r'stage1', ('production', 'stage')),
	(r'dev1', 'development'),

	(r'glados', ('development', 'glados')),
)

ADMINS = (
	('Project Lead', 'project_lead@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'USER': 'dbuser',
		'NAME': 'examplecom',
	}
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'v%eryyk0u!l^tsu0qzqoed@cucs!*3htobh$o2jf5ytz)a^2d^'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',
)

MEDIA_ROOT = '/var/www/example.com/media'

metasettings.init(globals())
