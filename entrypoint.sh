#!/bin/bash
set -e

echo "🚀 Démarrage de l'application Quincaillerie sur Railway..."
echo "📋 Settings utilisés : ${DJANGO_SETTINGS_MODULE:-config.settings.production}"

# Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

# Lancer Gunicorn
echo "✅ Lancement de Gunicorn sur le port ${PORT:-8080}..."
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8080}" \
    --log-file - \
    --access-logfile - \
    --error-logfile -