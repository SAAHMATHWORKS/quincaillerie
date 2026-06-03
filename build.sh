#!/usr/bin/env bash
# Installation des dépendances système pour WeasyPrint
apt-get update && apt-get install -y \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Collecte des fichiers statiques
python manage.py collectstatic --noinput