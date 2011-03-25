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

		# Move the settings into the local scope
		for (setting, setting_value) in settings.items():
			if setting == setting.upper():
				setattr(self, setting, setting_value)
