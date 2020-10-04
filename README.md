![Docker Compose UI](https://raw.githubusercontent.com/francescou/docker-compose-ui/master/static/images/logo-dark.png)

[![Docker Stars](https://img.shields.io/docker/stars/francescou/docker-compose-ui.svg)](https://hub.docker.com/r/francescou/docker-compose-ui/)
[![Docker Pulls](https://img.shields.io/docker/pulls/francescou/docker-compose-ui.svg)](https://hub.docker.com/r/francescou/docker-compose-ui/)

## What is it

Docker Compose UI is a web interface for Docker Compose.

The aim of this project is to provide a minimal HTTP API on top of Docker Compose while maintaining full interoperability with Docker Compose CLI.

The application can be deployed as a single container, there are no dependencies nor databases to install.

![compose ui screenshots](https://raw.githubusercontent.com/francescou/docker-compose-ui/master/screenshots/docker-compose-ui.gif)


## Compose file format compatibility matrix

| Compose file format  | Docker Engine |
| ------------- | ------------- |
| 3.8 | 19.03.0+ |
| 3.7 | 18.06.0+ |
| 3.6 | 18.02.0+ |
| 3.3 - 3.5 | 17.06.0+ |
| 3.0 – 3.2| 1.13.0+ |
| 2.3	| 17.06.0+ |
| 2.2	| 1.13.0+ |
| 2.1	| 1.12.0+ |
| 2.0	| 1.10.0+ |
| 1.0	| 1.9.1+ |

## Getting started

Run the following command in terminal:

    docker run \
    --name docker-compose-ui \
    -p 5000:5000 \
    -w /opt/docker-compose-projects/ \
    -v /var/run/docker.sock:/var/run/docker.sock \
    francescou/docker-compose-ui:1.13.0

You have to wait while Docker pulls the container from the Docker Hub: <https://hub.docker.com/r/francescou/docker-compose-ui/>

Then open your browser to `http://localhost:5000`

If you already have docker-compose installed, you can run `docker-compose up` and then open your browser to `http://localhost:8080`.


### Add your own docker-compose projects

to use your own docker-compose projects run this command from the directory containing your docker-compose.yml files:

    docker run \
        --name docker-compose-ui \
        -v $(pwd):$(pwd) \
        -w $(dirname $(pwd)) \
        -p 5000:5000 \
        -v /var/run/docker.sock:/var/run/docker.sock \
        francescou/docker-compose-ui:1.13.0

you can download my example projects into */home/user/docker-compose-ui/demo-projects/* from https://github.com/francescou/docker-compose-ui/tree/master/demo-projects

### Load projects from a git repository (experimental)

    docker run \
    --name docker-compose-ui \
    -p 5000:5000 \
    -w /opt/docker-compose-projects-git/ \
    -v /var/run/docker.sock:/var/run/docker.sock  \
    -e GIT_REPO=https://github.com/francescou/docker-compose-ui.git \
    francescou/docker-compose-ui:1.13.0

### Note about scaling services

Note that some of the services provided by the demo projects are not "scalable" with `docker-compose scale SERVICE=NUM` because of published ports conflicts.

Check out this project if you are interested in scaling up and down a docker-compose service without having any down time: <https://github.com/francescou/docker-continuous-deployment>


### Note about volumes

since you're running docker-compose inside a container you must pay attention to volumes mounted with relative paths, see [Issue #6](https://github.com/francescou/docker-compose-ui/issues/6)

### Integration with external web console

Docker Compose UI support to lauch a console with a shell (one of `/bin/bash` or `/bin/sh`) in a given container if a suitable companion container is available, the only requirement for a web console is to support passing the container id (or name) and the command to exec as querystring parameters.

For e.g. with [bitbull/docker-exec-web-console](https://github.com/bitbull-team/docker-exec-web-console) you can call `http://localhost:8888/?cid={containerName}&cmd={command}`, so you can pass the `WEB_CONSOLE_PATTERN` environment var to docker-compose-ui, that hold the pattern that will be used to build the url to load the console. Such pattern should include the `{containerName}` and `{command}` placeholders.

Example usage:

    docker run \
        --name docker_exec_web_console \
        -p 8888:8888 \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        -e 'CONTEXT_PATH=/web-console/' \
        bitbull/docker-exec-web-console

    docker run \
        --name docker-compose-ui \
        -p 5000:5000 \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        -e 'WEB_CONSOLE_PATTERN=http://localhost:8888/web-console/?cid={containerName}&cmd={command}' \
        francescou/docker-compose-ui:1.13.0


## Remote docker host

You can also run containers on a remote docker host, e.g.

    docker run \
        --name docker-compose-ui \
        -p 5000:5000 \
        -e DOCKER_HOST=remote-docker-host:2375 \
        francescou/docker-compose-ui:1.13.0


### Docker Swarm or HTTPS Remote docker host

The project has been tested against a Docker Engines 1.12 cluster ([swarm mode](https://docs.docker.com/engine/swarm/swarm-tutorial/)).

You need to add two environment properties to use an HTTPS remote docker host: `DOCKER_CERT_PATH` and `DOCKER_TLS_VERIFY`, see [example by @ymote](https://github.com/francescou/docker-compose-ui/issues/5#issuecomment-135697832)

### Authenticated docker registries

If your projects require you to pull images from a private docker registry that requires authentication, you will need to provide a `config.json` file with the necessary configuration options to the docker-compose-ui container at `/root/.docker/config.json`. You can generate the file on any host by performing `docker login [your private registry address]` and copying the resulting file from your ~/.docker directory to where it is needed.

For example:

    docker run \
        --name docker-compose-ui \
        -p 5000:5000 \
        -w /opt/docker-compose-projects/ \
        -v /home/user/.docker/config.json:/root/.docker/config.json:ro \
        francescou/docker-compose-ui:1.13.0

## Technologies

Docker Compose UI has been developed using Flask (python microframework) to provide RESTful services and AngularJS to implement the Single Page Application web ui.

The application uses [Docker Compose](https://docs.docker.com/compose) to monitor and edit the state of a set of docker compose projects (*docker-compose.yml* files).


## API

API docs at <https://francescou.github.io/docker-compose-ui/api.html>

## Issues

If you have any problems with or questions about this image, please open a GitHub issue on https://github.com/francescou/docker-compose-ui

## License - MIT

The Docker Compose UI code is licensed under the MIT license.

Docker Compose UI: Copyright (c) 2016 Francesco Uliana. www.uliana.it/francesco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


