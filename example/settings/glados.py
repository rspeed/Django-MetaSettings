#@PydevCodeAnalysisIgnore

# We know anything inherited won't be right, so just replace it outright
TEMPLATE_DIRS = ('/Users/bill/Sites/example/templates',)

MEDIA_ROOT = '/Users/bill/Sites/example/media'

DATABASES['default'].update({
	'USER': 'bill',
	'PASSWORD': 'billslousypw',
	'HOST': 'dev1',
	'NAME': 'examplecom_bill',
})