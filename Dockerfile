FROM python:3.12.3-slim

# Installer les dépendances système nécessaires à WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Collecter les fichiers statiques (aucune erreur si le dossier n'existe pas)
RUN python manage.py collectstatic --noinput

# Exposer le port (Railway utilise le port 8080 par défaut, mais Gunicorn écoute sur 8000 ; on peut le préciser)
EXPOSE 8000

# Lancer Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-"]