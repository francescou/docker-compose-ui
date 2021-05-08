# https://github.com/nsano-rururu/docker-compose-ui
# DOCKER-VERSION 19.03
FROM python:3.9.5-alpine AS builder
MAINTAINER Naoyuki Sano <nsano@ae.em-net.ne.jp>

RUN pip install virtualenv

RUN apk add -U --no-cache cargo \
    git \
    gcc \
    libffi-dev \
    make \
    musl-dev \
    openssl \
    openssl-dev

COPY ./requirements.txt /app/requirements.txt
RUN virtualenv /env && \
    /env/bin/python -m pip install --upgrade pip && \
    /env/bin/pip install --no-cache-dir cryptography && \
    /env/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
COPY demo-projects /opt/docker-compose-projects

FROM python:3.9.5-alpine

RUN apk add -U --no-cache git 

VOLUME ["/opt/docker-compose-projects"]

COPY --from=builder /env /env
COPY --from=builder /app /app
COPY --from=builder /opt/docker-compose-projects /opt/docker-compose-projects

EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/main.py"]

WORKDIR /opt/docker-compose-projects/
