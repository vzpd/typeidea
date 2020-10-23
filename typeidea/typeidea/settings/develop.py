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
