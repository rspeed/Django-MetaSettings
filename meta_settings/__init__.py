"""
Django MetaSettings

Licensed under the MIT License. See LICENSE.
http://creativecommons.org/licenses/MIT/
"""

import socket, re, os

HOSTNAME = 1
FQDN = 2
PATH = 3

class patterns():
	_import_complete = lambda self: len(self._settings.keys()) > 0

	def __init__(self, settings_dir):
		self._settings_dir = settings_dir
		self._settings = {}
		self._modules = []


	def add_modules(self, method, *patterns):
		if self._import_complete():
			raise RuntimeError('Settings already configured.')

		match = {
			HOSTNAME: lambda: socket.gethostname(),
			FQDN: lambda: socket.getfqdn(),
			PATH: lambda: None,
			None: lambda: None,
		}.get(method)()

		for pattern in patterns:
			if bool(re.match(pattern[0], match)):
				modules = pattern[1]

				# Make sure the list of modules is either a list or a tuple
				if type(modules) not in (list, tuple):
					modules = (modules,)

				# Add the modules to the module list
				self._modules += modules

				return

		raise Exception("No match for %s." % match)


	def import_settings(self, name):
			execfile('%s/%s.py' % (self._settings_dir, name), globals(), self._settings)


	def get_settings(self):
		# Only import the modules once
		if not self._import_complete():
			self.import_settings('base')

			for module in self._modules:
				self.import_settings(module)

		# Only return settings with upper-case names
		return dict([(setting, self._settings[setting]) for setting in self._settings.keys() if setting.isupper()])
