FROM python:3.11-slim

WORKDIR /products-management

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /products-management/src

EXPOSE 5002

ENV PORT 5002

CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0", "--port=5002"]