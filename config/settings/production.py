import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.railway.app', '.up.railway.app']

# PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
else:
    # Fallback : reconstruire l'URL à partir des variables individuelles
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PGDATABASE', 'railway'),
            'USER': os.environ.get('PGUSER', 'postgres'),
            'PASSWORD': os.environ.get('PGPASSWORD', os.environ.get('POSTGRES_PASSWORD', '')),
            'HOST': os.environ.get('PGHOST', os.environ.get('POSTGRES_HOST', 'localhost')),
            'PORT': os.environ.get('PGPORT', '5432'),
        }
    }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True