# https://github.com/francescou/docker-compose-ui
# DOCKER-VERSION 1.12.3
FROM python:2.7-alpine
MAINTAINER Francesco Uliana <francesco@uliana.it>

RUN pip install virtualenv

RUN apk add -U --no-cache git

COPY ./requirements.txt /app/requirements.txt
RUN virtualenv /env && /env/bin/pip install --no-cache-dir -r /app/requirements.txt

VOLUME /app

VOLUME ["/opt/docker-compose-projects"]

COPY demo-projects /opt/docker-compose-projects

EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/main.py"]

WORKDIR /opt/docker-compose-projects/