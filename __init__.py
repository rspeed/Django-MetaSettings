"""
Django MetaSettings

Licensed under the MIT License. See LICENSE.
http://creativecommons.org/licenses/MIT/
"""
import os, re

def _get_hostname():
	hostname = os.uname()[1]

	# Convert the machine's hostname into alphanumeric characters
	# Note: We don't want to use \W because it also matches underscores.
	#       The string segment "._." would end up as "___" instead of "_".
	hostname = re.sub('[^a-zA-Z0-9]+', '_', hostname)

	return hostname


def import_via_hostname(parent_locals):
	import_settings(_get_hostname(), parent_locals)


def import_via_hostname_dict(hostnames):
	import_settings(hostnames.get(_get_hostname()), parent_locals)


def import_settings(module, parent_locals):
	# If the requested settings file isn't found, default to the production settings
	try:
		_get_settings(module)
	except ImportError:
		#TODO Raise a warning
		module = 'production'

	# Load the config settings properties into the local scope
	for key, value in _climb_settings(module).items():
		parent_locals[key] = value


def _climb_settings(name):
	# Import the configuration settings file
	settings = _get_settings(name)

	parent_module_name = settings.get('EXTENDS')
	if parent_module_name is None:
		return settings
	else:
		del settings['EXTENDS']
		parent_settings = import_settings(parent_module_name)
		parent_settings.update(settings)
		return parent_settings


def _get_settings(name):
	settings = {}
	settings_module = __import__('settings.%s' % name, globals(), locals(), 'settings')

	for setting in dir(settings_module):
		if setting.isupper():
			settings[setting] = getattr(settings_module, setting)

	return settings



