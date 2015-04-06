from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'college_football_fantasy',
        'USER': 'zackjcooper',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}
