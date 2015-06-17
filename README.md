# Docker Compose UI

    docker run \
    --name docker-compose-ui \
    -p 5000:5000 \
    -v /home/user/docker-compose-projects:/opt/definitions \
    -e DOCKER_HOST=my-host:5915 \
    docker-compose-ui
