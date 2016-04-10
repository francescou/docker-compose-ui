# https://github.com/francescou/docker-compose-ui
# DOCKER-VERSION 1.10.3
FROM python:2.7-slim
MAINTAINER Francesco Uliana <francesco@uliana.it>

RUN pip install virtualenv
RUN apt-get update && apt-get install -y git

WORKDIR /app
RUN virtualenv /env
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r requirements.txt
ADD . /app

VOLUME ["/opt/docker-compose-projects"]

COPY demo-projects /opt/docker-compose-projects

EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/main.py"]
