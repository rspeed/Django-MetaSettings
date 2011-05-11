"""
Django MetaSettings

Licensed under the MIT License. See LICENSE.
http://creativecommons.org/licenses/MIT/
"""

import socket
import re
import os


HOSTNAME = 'METASETTINGS_MATCHING_METHOD_HOST_NAME'
FQDN = 'METASETTINGS_MATCHING_METHOD_DOMAIN_NAME'
ENV = 'METASETTINGS_MATCHING_METHOD_ENVIRONMENTAL_VARIABLE'
VAR = 'METASETTINGS_MATCHING_METHOD_SETTINGS_VAR'


def init(_globals):
	# The method used for matching
	meta_method = _globals.get("METASETTINGS_METHOD", HOSTNAME)

	# The directory where settings files are stored
	meta_dir = _globals.get("METASETTINGS_DIR", 'settings')

	# The list of patterns to match against, defaults to doing nothing
	meta_patterns = _globals.get("METASETTINGS_PATTERNS", (r'.*', []))


	# Name of the environment variable containing the key for ENV matching
	env_name = _globals.get("METASETTINGS_ENV_NAME", 'METASETTINGS_KEY')

	# Name of the settings variable containing the value for VAR matching
	path_var_name = _globals.get("METASETTINGS_VAR_NAME", "PROJECT_PATH")


	# Determine the matching method and get the value to match against
	match = {
		HOSTNAME: lambda: socket.gethostname(),
		FQDN: lambda: socket.getfqdn(),
		ENV: lambda: os.getenv(env_name),
		VAR: lambda: _globals.get('PROJECT_PATH'),
		None: lambda: None,
	}.get(meta_method)()

	# Match the environment
	modules = [pattern[1] for pattern in meta_patterns if re.match(pattern[0], match)]

	if len(modules) == 0:
		raise Exception("No match for %s." % match)

	# There may be more than one match, default to the first
	modules = modules[0]

	# Make sure the list of modules is iterable
	if not hasattr(modules, '__iter__'):
		modules = (modules,)

	full_meta_dir = os.path.join(os.path.dirname(_globals['__file__']), meta_dir)
	for module in modules:
		execfile('%s/%s.py' % (full_meta_dir, module), _globals)
