from .base import *

DEBUG = False

DATABASES = {
    'default': env.db()   # prend DATABASE_URL
}

# Sécurité HTTPS (Render s'en occupe, mais on peut garder)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# WhiteNoise est déjà configuré dans base.py