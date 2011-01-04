
TEMPLATE_DIRS = (
	'/Library/WebServer/www/example.com/app/templates/'
)

MEDIA_ROOT = '/Library/WebServer/example.com/media/'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': '/Library/WebServer/example.com/db/default.sqlite',
	}
}
