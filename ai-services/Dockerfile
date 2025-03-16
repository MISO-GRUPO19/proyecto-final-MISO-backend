FROM python:3.11-slim

WORKDIR /ai-services

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /ai-services/src

EXPOSE 5006

ENV PORT 5006

# Variables de entorno para Uptrace
ENV UPTRACE_DSN=https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872

CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=5006"]