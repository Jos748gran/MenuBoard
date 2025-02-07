import os
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Restaurante',
        'USER': 'postgres',
        'PASSWORD': 'settings.PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}