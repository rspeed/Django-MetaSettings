"""
Django MetaSettings

Licensed under the MIT License. See LICENSE.
http://creativecommons.org/licenses/MIT/
"""
import socket, re

def get_hostname():
	# Convert the machine's hostname into alphanumeric characters, suitable for python module names
	# Note: We don't want to use \w because it also matches underscores.
	#       The string segment "._." would end up as "___" instead of "_".
	return re.sub('[^a-zA-Z0-9]+', '_', socket.gethostname())


def import_settings(module):
	# If the requested settings file isn't found, default to the production settings
	try:
		_get_settings(module)
	except ImportError:
		#TODO Raise a warning
		module = 'production'

	# Load the config settings properties into the local scope
	return _climb_settings(module)


def _climb_settings(name):
	# Import the configuration settings file
	settings = _get_settings(name)

	parent_module_name = settings.get('EXTENDS')
	if parent_module_name is None:
		return settings
	else:
		del settings['EXTENDS']
		return dict(_get_settings(parent_module_name), **settings)


def _get_settings(name):
	settings = {}
	settings_module = __import__('settings.%s' % name, globals(), locals(), 'settings')

	for setting in dir(settings_module):
		if setting.isupper():
			settings[setting] = getattr(settings_module, setting)

	return settings



