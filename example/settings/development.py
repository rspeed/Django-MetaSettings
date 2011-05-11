#@PydevCodeAnalysisIgnore

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS += (
	('Development Lead', 'devlead@example.com'),
	('Development Team', 'devteam@example.com'),
)
MANAGERS = ADMINS

MEDIA_URL = '/media'

DATABASES['default'].update({
	'USER': 'test1',
	'PASSWORD': 'testpw',
	'NAME': 'examplecom_dev1',
})