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

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Rendre le script exécutable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Lancer le entrypoint
ENTRYPOINT ["./entrypoint.sh"]