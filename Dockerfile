FROM python:3.8-alpine

RUN apk add --no-cache build-base postgresql-dev openssl-dev libffi-dev

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV FLASK_APP=/app/application/application.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

ENTRYPOINT ["/app/docker-entrypoint.sh"]
