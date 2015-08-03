# Docker Compose UI

## What is it

Docker Compose UI is a web interface for Docker Compose.
Disclaimer: the software is still under heavy development and might not be ready for production use.

![screenshot project detail](https://raw.githubusercontent.com/francescou/docker-compose-ui/master/screenshots/project-detail.png)


![screenshot remote docker host](https://raw.githubusercontent.com/francescou/docker-compose-ui/master/screenshots/remote-host.png)

# Requirements

Docker 1.6.0 or later

## Getting started

Put some docker-compose projects in a directory (you can checkout my example projects into /home/user/docker-compose-ui/demo-projects/ from https://github.com/francescou/docker-compose-ui/tree/master/demo-projects) and then run:

    docker run \
    --name docker-compose-ui \
    -p 5000:5000 \
    -v /home/user/docker-compose-ui/demo-projects:/opt/docker-compose-projects:ro \
    -v /var/run/docker.sock:/var/run/docker.sock \
    francescou/docker-compose-ui

Open your browser to `http://localhost:5000`

### Remote docker host

You can also run containers on a remote docker host, e.g.

    docker run \
        --name docker-compose-ui \
        -p 5000:5000 \
        -v /home/user/docker-compose-ui/demo-projects:/opt/docker-compose-projects:ro \
        -e DOCKER_HOST=remote-docker-host:2375 \
        francescou/docker-compose-ui

## Technologies

Docker Compose UI has been developed using Flask (python microframework) to provide RESTful services and AngularJS to implement the Single Page Application web ui.

The application uses [Docker Compose](https://docs.docker.com/compose) to monitor and edit the state of a set of docker compose projects (*docker-compose.yml* files).


## API

### list docker compose projects

    curl http://localhost:5000/api/v1/projects

### show docker compose "hello-node" project details

    curl http://localhost:5000/api/v1/projects/hello-node

### docker-compose up of project "hello-node"

    curl -X POST http://localhost:5000/api/v1/projects --data '{"id":"hello-node"}' -H'Content-type: application/json'

### docker-compose build of project "hello-node"

    curl -X POST http://localhost:5000/api/v1/build --data '{"id":"hello-node"}' -H'Content-type: application/json'

### docker-compose update of project "hello-node"

    curl -X PUT http://localhost:5000/api/v1/projects --data '{"id":"hello-node"}' -H'Content-type: application/json'

### docker-compose kill of project "hello-node"

    curl -X DELETE http://localhost:5000/api/v1/projects/hello-node

### docker-compose logs of project "hello-node"

    curl http://localhost:5000/api/v1/logs/hello-node/100

### authentication status

    curl http://localhost:5000/api/v1/authentication

### set password

    curl -X POST -u admin  http://localhost:5000/api/v1/authentication -H 'Content-type: application/json' --data  '{"username":"admin", "password":"password"}'

### disable basic authentication

    curl -X DELETE -u admin  http://localhost:5000/api/v1/authentication

## License - MIT

The Docker Compose UI code is licensed under the MIT license.

Docker Compose UI: Copyright (c) 2015 Francesco Uliana. www.uliana.it/francesco

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


