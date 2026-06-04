#!/bin/sh

set -e  # Arrêter le script en cas d'erreur

echo "🚀 Démarrage de l'application Quincaillerie sur Railway..."

# ======================
# Préparations
# ======================

echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "👥 Initialisation des groupes (si nécessaire)..."
python manage.py init_groups

# ======================
# Lancement de Gunicorn
# ======================

echo "✅ Lancement de Gunicorn sur le port ${PORT:-8080}..."

exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8080}" \
    --workers 3 \
    --threads 2 \
    --log-file - \
    --access-logfile - \
    --error-logfile -