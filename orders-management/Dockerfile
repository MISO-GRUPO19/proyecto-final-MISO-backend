# Usar una imagen base de Python
FROM python:3.11-slim

WORKDIR /orders-management

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /orders-management/src

EXPOSE 5001
# Comando para ejecutar la aplicación Flask
CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=5001"]