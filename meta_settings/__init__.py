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
	def __init__(self, method, locals, *patterns):
		self.settings_dir = os.path.dirname(os.path.abspath(locals['__file__']))
		self.settings = locals

		match = {
			HOSTNAME: lambda: socket.gethostname(),
			FQDN: lambda: None,
			PATH: lambda: None,
			None: lambda: None,
		}.get(method)()

		for pattern in patterns:
			if bool(re.match(pattern[0], match)):
				self.modules = pattern[1]
				return

		raise Exception("No match for %s." % match)


	def import_settings(self):
		for module in self.modules:
			execfile('%s/%s.py' % (self.settings_dir, module), globals(), self.settings)

		# Only return settings with upper-case names
		return dict([(setting, self.settings[setting]) for setting in self.settings.keys() if setting.isupper()])
