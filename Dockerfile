FROM python:3.12.3-slim

# Dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Rendre le entrypoint exécutable
RUN chmod +x entrypoint.sh

# Lancer l'application
CMD ["./entrypoint.sh"]