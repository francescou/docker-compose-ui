# https://github.com/francescou/docker-compose-ui
# DOCKER-VERSION 1.11.2
FROM python:2.7-alpine
MAINTAINER Francesco Uliana <francesco@uliana.it>

RUN pip install virtualenv

RUN apk add --update git && rm -rf /var/cache/apk/*

COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

VOLUME ["/opt/docker-compose-projects"]

COPY demo-projects /opt/docker-compose-projects

EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/main.py"]
