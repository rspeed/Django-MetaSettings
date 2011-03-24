# Configure Django MetaSettings
import metasettings

METASETTINGS_METHOD = metasettings.HOSTNAME

METASETTINGS_DIR = 'settings'

METASETTINGS_PATTERNS = (
	(r'production1', 'production'),
	(r'stage1', ('production', 'stage')),
	(r'dev1', ('development')),

	(r'glados', ('development', 'glados')),
	(r'server.8207std.private', ('base', 'development', 'glados'))
)