from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-oj+n%_)eec15&slf$*#1*api7q+@r2b=gtofcx*ay%+2mmf&r^'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.104']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'funcional',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'joaquin',
    }
}

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')