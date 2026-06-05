#!/bin/bash
set -e

echo "🚀 Démarrage de l'application Quincaillerie sur Railway..."
echo "📋 Settings utilisés : ${DJANGO_SETTINGS_MODULE:-config.settings.production}"

# Debug : afficher les variables PostgreSQL (sans le mot de passe)
echo "🔍 Variables d'environnement :"
echo "   DATABASE_URL = ${DATABASE_URL:+définie}"
echo "   PGHOST = ${PGHOST:-non définie}"
echo "   PGPORT = ${PGPORT:-5432}"
echo "   PGDATABASE = ${PGDATABASE:-non définie}"
echo "   PGUSER = ${PGUSER:-non définie}"

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