# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'ReplaceItWithSecretString'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = False
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
	'kay.auth',
	'core',
	#'json_test',
)

APP_MOUNT_POINTS = {
	'core':'/',
	#'json_test':'/json_test',
}

# You can remove following settings if unnecessary.
CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
  'kay.auth.context_processors.login_box',
)

MIDDLEWARE_CLASSES = (
  'kay.sessions.middleware.SessionMiddleware',
  'kay.auth.middleware.AuthenticationMiddleware',
)

AUTH_USER_BACKEND = 'kay.auth.backends.datastore.DatastoreBackend'
AUTH_USER_MODEL = 'core.models.MyUser'

