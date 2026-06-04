#!/bin/sh

echo "🚀 Démarrage de l'application Quincaillerie..."

# Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Initialiser les groupes (si nécessaire)
echo "👥 Initialisation des groupes d'utilisateurs..."
python manage.py init_groups

echo "✅ Démarrage de Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --threads 2 \
    --log-file - \
    --access-logfile - \
    --error-logfile -