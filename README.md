# Docker Compose UI

    docker run \
    --name docker-compose-ui \
    -p 5000:5000 \
    -v /home/user/docker-compose-projects:/opt/docker-compose-projects \
    -e DOCKER_HOST=my-host:5915 \
    docker-compose-ui


# Temp

docker run --rm --name docker-compose-ui -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock -v /home/francesco/foobar/:/opt/docker-compose-projects:ro docker-compose-ui

# API

curl http://localhost:5000/api/v1/containers

curl http://localhost:5000/api/v1/containers/compose-mongo

curl -X POST http://localhost:5000/api/v1/containers --data '{"id":"compose-mongo"}' -H'Content-type: application/json'

curl -X PUT http://localhost:5000/api/v1/containers --data '{"id":"compose-mongo"}' -H'Content-type: application/json'

curl -X DELETE http://localhost:5000/api/v1/containers/compose-mongo

curl http://localhost:5000/api/v1/logs/compose-mongo/100