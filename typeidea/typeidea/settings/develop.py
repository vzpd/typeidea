from .base import * # NOQA

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST':{
            'CHARSET':'utf8',
            'COLLATION':'utf8_general_ci'
            }
    }
}

INSTALLED_APPS += [
        'debug_toolbar',
    ]

MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

INTERNAL_IPS = ['127.0.0.1', '192.168.99.100']
