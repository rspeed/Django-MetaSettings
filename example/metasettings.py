import meta_settings
from django.conf import settings

patterns = meta_settings.patterns('settings')

patterns.add_modules(
	meta_settings.HOSTNAME,
	(r'production1', 'production'),
	(r'stage1', ('production', 'stage')),
	(r'dev1', ('development')),

	(r'glados', ('development', 'glados')),
)

# Pull the merged settings and pass them to settings.configure
settings.configure( **patterns.get_settings() )
