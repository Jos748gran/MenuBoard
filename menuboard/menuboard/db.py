import os
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_miguelon',
        'USER': 'postgres',
        'PASSWORD': 'cancer50',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}