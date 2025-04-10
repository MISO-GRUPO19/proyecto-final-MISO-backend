FROM python:3.11-slim

WORKDIR /products_management

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-sdk

COPY . .

# Configurar las credenciales de Google Cloud
ARG GOOGLE_CREDENTIALS_BASE64
ENV GOOGLE_APPLICATION_CREDENTIALS=/products_management/src/pubsub/proyecto-final-451719-1806c6f593e4.json

RUN if [ ! -z "$GOOGLE_CREDENTIALS_BASE64" ]; then \
    echo $GOOGLE_CREDENTIALS_BASE64 | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS; \
    else echo "GOOGLE_CREDENTIALS_BASE64 no está definido, omitiendo credenciales."; \
    fi

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /products_management/src

EXPOSE 5002

ENV PORT 5002

ENV PYTHONPATH=/products_management/src

# Variables de entorno para Uptrace
ENV UPTRACE_DSN=https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872

# Script de inicio para ejecutar ambos procesos
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]