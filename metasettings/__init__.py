"""
Django MetaSettings

Licensed under the MIT License. See LICENSE.
http://creativecommons.org/licenses/MIT/
"""

import socket
import re
import os
import time
import django.conf
from django.conf import global_settings
from django.utils import importlib

HOSTNAME = 'METASETTINGS_MATCHING_METHOD_HOST_NAME'
FQDN = 'METASETTINGS_MATCHING_METHOD_DOMAIN_NAME'
PATH = 'METASETTINGS_MATCHING_METHOD_ROOT_PATH'
ENV = 'METASETTINGS_MATCHING_METHOD_ENVIRONMENTAL_VARIABLE'

# Name of the environment variable containing the key for ENV matching
ENV_NAME = 'METASETTINGS_KEY'

def init():
	"""
	Initialize Django MetaSettings by replacing django.conf.settings with a MetaSettings object.
	"""
	django.conf.Settings = MetaSettings


class MetaSettings(django.conf.Settings):
	def __init__(self, settings_module):
		# Run the standard settings import
		super(MetaSettings, self).__init__(settings_module)

		meta_method = getattr(self, "METASETTINGS_METHOD", HOSTNAME) # Default to hostname matching
		meta_dir = getattr(self, "METASETTINGS_DIR", self.SETTINGS_MODULE) # Default to the name of the settings module
		meta_patterns = getattr(self, "METASETTINGS_PATTERNS", (None, [])) # Default to something that just doesn't work

		match = {
			HOSTNAME: lambda: socket.gethostname(),
			FQDN: lambda: socket.getfqdn(),
			PATH: lambda: None,
			ENV: lambda: os.getenv(ENV_NAME),
			None: lambda: None,
		}.get(meta_method)()

		# Match the environment
		modules = [pattern[1] for pattern in meta_patterns if re.match(pattern[0], match)]

		if len(modules) == 0:
			raise Exception("No match for %s." % match)

		# There may be more than one match, default to the first
		modules = modules[0]

		# Make sure the list of modules is iterable
		if type(modules) not in (list, tuple):
			modules = (modules,)

		# Initialize a settings dictionary to maintain scope between settings files
		settings = dict((key, getattr(self, key)) for key in dir(self))

		for module in modules:
			execfile('%s/%s.py' % (meta_dir, module), globals(), settings)

		# The rest is copied from django.conf.Settings with a few minor tweaks

		tuple_settings = ("INSTALLED_APPS", "TEMPLATE_DIRS")

		for (setting, setting_value) in settings.items():
			if setting == setting.upper():
				if setting in tuple_settings and type(setting_value) == str:
					setting_value = (setting_value,) # In case the user forgot the comma.
				setattr(self, setting, setting_value)

		# Expand entries in INSTALLED_APPS like "django.contrib.*" to a list
		# of all those apps.
		new_installed_apps = []
		for app in self.INSTALLED_APPS:
			if app.endswith('.*'):
				app_mod = importlib.import_module(app[:-2])
				appdir = os.path.dirname(app_mod.__file__)
				app_subdirs = os.listdir(appdir)
				app_subdirs.sort()
				name_pattern = re.compile(r'[a-zA-Z]\w*')
				for d in app_subdirs:
					if name_pattern.match(d) and os.path.isdir(os.path.join(appdir, d)):
						new_installed_apps.append('%s.%s' % (app[:-2], d))
			else:
				new_installed_apps.append(app)
		self.INSTALLED_APPS = new_installed_apps

		if hasattr(time, 'tzset') and self.TIME_ZONE:
			# When we can, attempt to validate the timezone. If we can't find
			# this file, no check happens and it's harmless.
			zoneinfo_root = '/usr/share/zoneinfo'
			if (os.path.exists(zoneinfo_root) and not
					os.path.exists(os.path.join(zoneinfo_root, *(self.TIME_ZONE.split('/'))))):
				raise ValueError("Incorrect timezone setting: %s" % self.TIME_ZONE)
			# Move the time zone info into os.environ. See ticket #2315 for why
			# we don't do this unconditionally (breaks Windows).
			os.environ['TZ'] = self.TIME_ZONE
			time.tzset()

		# Settings are configured, so we can set up the logger if required
		if self.LOGGING_CONFIG:
			# First find the logging configuration function ...
			logging_config_path, logging_config_func_name = self.LOGGING_CONFIG.rsplit('.', 1)
			logging_config_module = importlib.import_module(logging_config_path)
			logging_config_func = getattr(logging_config_module, logging_config_func_name)

			# ... then invoke it with the logging settings
			logging_config_func(self.LOGGING)
