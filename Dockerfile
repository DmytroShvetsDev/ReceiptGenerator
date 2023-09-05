FROM python:3.10-slim
LABEL maintainer="dmytroshvetsdev@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/media/pdf


RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

RUN chown -R django-user:django-user /app
RUN chmod -R 755 /app

USER django-user
