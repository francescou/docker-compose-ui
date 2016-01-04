# https://github.com/francescou/docker-compose-ui
# DOCKER-VERSION 1.9.1
FROM python:2.7.11-slim
MAINTAINER Francesco Uliana <francesco@uliana.it>

RUN apt-get update
RUN apt-get install -y build-essential

WORKDIR /app
RUN virtualenv /env
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r requirements.txt
ADD . /app

VOLUME ["/opt/docker-compose-projects"]

COPY demo-projects /opt/docker-compose-projects

EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/runserver.py"]
