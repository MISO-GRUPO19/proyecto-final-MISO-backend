# Usar una imagen base de Python
FROM python:3.11-slim

WORKDIR /orders-management

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /orders-management/src

EXPOSE 5001

# Establecer la variable de entorno PORT
ENV PORT 5001

# Variables de entorno para Uptrace
ENV UPTRACE_DSN=https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872

# Comando para ejecutar la aplicación Flask
CMD ["flask", "--app", "main.py", "--debug", "run", "--host=0.0.0.0", "--port=5001"]