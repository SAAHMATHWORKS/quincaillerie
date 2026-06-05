import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.railway.app', '.up.railway.app']

# PostgreSQL - essayer plusieurs méthodes
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Méthode Railway recommandée
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
    print("✅ PostgreSQL connecté via DATABASE_URL")
else:
    # Fallback : variables séparées
    PGHOST = os.environ.get('PGHOST')
    if PGHOST:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('PGDATABASE', 'railway'),
                'USER': os.environ.get('PGUSER', 'postgres'),
                'PASSWORD': os.environ.get('PGPASSWORD', ''),
                'HOST': PGHOST,
                'PORT': os.environ.get('PGPORT', '5432'),
            }
        }
        print("✅ PostgreSQL connecté via variables séparées")
    else:
        raise Exception("Aucune configuration PostgreSQL trouvée !")

# Sécurité HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True