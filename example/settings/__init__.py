SETTINGS_MODULE = "settings"

import metasettings

settings = metasettings.MetaSettings(SETTINGS_MODULE)

settings.add_modules(
	metasettings.HOSTNAME,
	(r'production1', 'production'),
	(r'stage1', ('production', 'stage')),
	(r'dev1', ('development')),

	(r'glados', ('development', 'glados')),
)

settings.configure()