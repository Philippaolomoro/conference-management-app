FROM python:3.9.4-alpine
MAINTAINER Philippa Olomoro

WORKDIR /source

ENV PYTHONDONRWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /source/requirements.txt

RUN apk add build-base
RUN set -eux \
    && apk add --update --no-cache --virtual .tmp-build-deps \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev bash \
    && pip install --upgrade pip \
    && pip install -r /source/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /source
