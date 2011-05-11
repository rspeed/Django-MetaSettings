# Django-MetaSettings

Simplify the obnoxious task of configuring the same Django project in multiple environments.

## About

Django MetaSettings allows you to place settings specific to different environments into separate files. Based on certain environmental conditions different settings can be loaded from multiple sources.

## Installation

### Create the environment specific settings files

Start by creating a folder to store the settings files. Since Django MetaSettings doesn't use ``import``, so the folder doesn't need to be a package. You can call the folder anything you want, but settings is recommended for the sake of simplicity.

``mkdir settings``

Create a python script for each set of environmental conditions, containing the apropriate settings. For example, development.py might enable debugging and debug_toolbar.

``` python
"""
development.py
Settings for development systems.
"""

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += (
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
	'debug_toolbar',
)
```

Additionally, you may want to create a settings file for each machine the application will run on.

``` python
"""
glados.py
Settings for the system identified as GLaDOS.
"""

DATABASE_USER = 'dbuser'
DATABASE_PASSWORD = 'dbpassword'

MEDIA_ROOT = '/var/www/test/assets'
MEDIA_URL = '/assets/'
ADMIN_MEDIA_PREFIX = '/assets/admin/'

TEMPLATE_DIRS = (
	"/var/www/test/templates",
)
```

### Install the module

**PIP** ``pip install django-metasettings`` or **easy_install** ``easy_install django-metasettings``

### Modify the project's settings.py

You can declare the METASETTINGS_* entries where you want in the ``settings.py`` file, but the line starting with ``metasettings.init`` should be at the end of the file.

All settings after this line will overload those loaded with Django MetaSettings


``` python
import metasettings
METASETTINGS_METHOD = metasettings.HOSTNAME
METASETTINGS_DIR = 'settings'
METASETTINGS_PATTERNS = (
	(r'hostname', ('base',),
)
metasettings.init(globals())
```
