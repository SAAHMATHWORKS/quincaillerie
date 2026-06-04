FROM python:3.12.3-slim

# Installer les dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Utilisation de la forme SHELL pour que $PORT soit bien interprété par Railway
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -