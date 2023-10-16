from .base import *

DATABASES = {
    'default': {
        'ENGINE': env.str('ENGINE'),
        'NAME': env.str('NAME'),
        'USER': env.str('USER_NAME'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': env.str('HOST'),
        'PORT': env.str('PORT'),
    }
}


ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SECRET_KEY = 'test'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': ''
    },
    'redis': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
