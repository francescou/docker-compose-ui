# Docker Compose demo projects

This directory contains several Docker Compose sample projects showing basic docker/docker-compose capabilities such as port publishing, container linking, volume mounting.

Note that some of the services provided by these projects are not "scalable" with `docker-compose scale SERVICE=NUM` because of port publish conflicts.

Check out this project if you are interested in scaling up and down a docker-compose service without having any down time: https://github.com/francescou/consul-template-docker-compose