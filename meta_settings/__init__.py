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
	def __init__(self, method, settings_dir, *patterns):
		self._settings_dir = settings_dir
		self._settings = {}

		match = {
			HOSTNAME: lambda: socket.gethostname(),
			FQDN: lambda: None,
			PATH: lambda: None,
			None: lambda: None,
		}.get(method)()

		for pattern in patterns:
			if bool(re.match(pattern[0], match)):
				self._modules = pattern[1]

				# Make sure the list of modules is either a list or a tuple
				if type(self._modules) not in (list, tuple):
					self._modules = (self._modules,)

				return

		raise Exception("No match for %s." % match)

	def import_settings(self, name):
			execfile('%s/%s.py' % (self._settings_dir, name), globals(), self._settings)


	def settings(self):
		self.import_settings('base')

		for module in self._modules:
			self.import_settings(module)

		# Only return settings with upper-case names
		return dict([(setting, self._settings[setting]) for setting in self._settings.keys() if setting.isupper()])
