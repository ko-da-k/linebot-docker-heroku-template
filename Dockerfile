FROM kyobad/miniconda3-alpine:latest

MAINTAINER K.Kato

RUN pip install --upgrade pip \
    && conda install -y flask \
    && pip install flask gunicorn line-bot-sdk \
    && adduser -D botter \
    && mkdir /home/botter/app

USER botter

WORKDIR /home/botter/app

CMD ["/bin/sh", "-c", "gunicorn bot:app --log-file=-"]