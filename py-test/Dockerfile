FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir confluent-kafka[json]==2.13.0

COPY consumer.py producer.py ca.pem /app/

