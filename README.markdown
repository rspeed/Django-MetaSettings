# Django-MetaSettings

Simplify the obnoxious task of configuring the same Django project in multiple environments.

## About

Django MetaSettings allows you to place settings specific to different environments into separate files. Based on certain environmental conditions different settings can be loaded from multiple sources.

## Installation

### Create the environment specific settings files

Start by creating a folder to store the settings files. Django MetaSettings doesn't use ``import``, so the folder doesn't need to be a package. You can call the folder anything you want, but "settings" is likely the most intuitive choice.

``mkdir settings``

Create a python script for each set of environmental conditions, containing the apropriate settings. For example, development.py might enable debugging and the Django Debug Toolbar.

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

**Note**: Your source code editor may show warnings when modifying variables like "INSTALLED_APPS" because the scope is shared between all of the settings files. You can safely ignore these warnings as long as the variable is initialized in a file loaded before the current one. In this case, because "MIDDLEWARE_CLASSES" and "INSTALLED_APPS" are initialized in settings.py.

Additionally, you may want to create a settings file for each machine the application will run on.

``` python
"""
glados.py
Settings for the system identified as GLaDOS.
"""

DATABASES['default'].update({
    'USER': 'dbuser',
    'PASSWORD': 'dbpassword',
    'NAME': 'example_testing_db_1'
})

MEDIA_ROOT = '/var/www/test/assets'
MEDIA_URL = '/assets/'
ADMIN_MEDIA_PREFIX = '/assets/admin/'

TEMPLATE_DIRS = (
    '/var/www/test/templates',
)
```

### Install the module

**PIP** ``pip install django-metasettings`` or **easy_install** ``easy_install django-metasettings``

### Modify the project's settings.py

``` python
import metasettings

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

METASETTINGS_METHOD = metasettings.HOSTNAME
METASETTINGS_DIR = PROJECT_PATH + '/settings'
METASETTINGS_PATTERNS = (
    ('glados': ('development', 'glados')),
    ('mainhost1', ('production', 'mainhost1)),
)

metasettings.init(globals())
```

You can declare the METASETTINGS_* entries where you want in the ``settings.py`` file, but the line starting with ``metasettings.init`` should be at the end. All settings after this line will override those loaded with Django MetaSettings.


#### METASETTINGS_METHOD

The possible values for METASETTINGS_METHOD are:

**metasettings.HOSTNAME:** Match against the server's hostname.

**metasettings.FQDN:** Match against the server's fully qualified domain name.

**metasettings.ENV:** Match against an environmental variable. See *METASETTINGS_ENV_NAME* below.

**metasettings.VAR:** Match against a settings variable. See *METASETTINGS_VAR_NAME* below.

#### METASETTINGS_DIR

This is the path to the directory where settings files are store. It defaults to "settings", but it's recommended that you provide a full path by setting and using "PROJECT_PATH".

#### METASETTINGS_PATTERNS

A list of lists to determine which settings files to load. The first value in each list is a regular expression pattern to test. The second value is a list of modules (located within the settings directory) to load. If there is only one module, a string can be substituted for the list.

**Note** If multiple patterns match, only the first will be used.

#### METASETTINGS_ENV_NAME

The name of the environmental variable to use for ENV matching. Defaults to "METASETTINGS_KEY" if not set.

#### METASETTINGS_VAR_NAME

The name of the settings variable to use for VAR matching. Defaults to "PROJECT_PATH" if not set.
