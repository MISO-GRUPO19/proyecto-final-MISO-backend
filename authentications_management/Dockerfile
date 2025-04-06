FROM python:3.11-slim

WORKDIR /authentications_management

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configurar las credenciales de Google Cloud
ARG GOOGLE_CREDENTIALS_BASE64
ENV GOOGLE_APPLICATION_CREDENTIALS=/authentications_management/src/pubsub/proyecto-final-451719-1806c6f593e4.json

RUN if [ ! -z "$GOOGLE_CREDENTIALS_BASE64" ]; then \
    echo $GOOGLE_CREDENTIALS_BASE64 | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS; \
    else echo "GOOGLE_CREDENTIALS_BASE64 no está definido, omitiendo credenciales."; \
    fi


ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /authentications_management/src

EXPOSE 5003

ENV PORT 5003

# Variables de entorno para Uptrace
ENV UPTRACE_DSN=https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872


# Script de inicio para ejecutar ambos procesos
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]