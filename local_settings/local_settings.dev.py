# -*- coding: utf-8 -*-

EXTRA_MIDDLEWARE_CLASSES = ( 
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

EXTRA_INSTALLED_APPS = ( 
    'debug_toolbar',
)

#For testing with Twill
DEBUG_PROPAGATE_EXCEPTIONS = True

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "dev.db",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

SITE_DOMAIN = "127.0.0.1:8000"