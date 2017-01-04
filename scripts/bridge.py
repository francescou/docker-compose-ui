"""
bridge to docker-compose
"""

import logging
from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment

from compose.cli.docker_client import docker_client
from compose.const import API_VERSIONS
from compose.config.config import V2_0

def ps_(project):
    """
    containers status
    """
    logging.debug('ps ' + project.name)
    containers = project.containers(stopped=True)

    items = [{
        'name': container.name,
        'name_without_project': container.name_without_project,
        'command': container.human_readable_command,
        'state': container.human_readable_state,
        'labels': container.labels,
        'ports': container.ports,
        'volumes': get_volumes(get_container_from_id(project.client, container.id)),
        'is_running': container.is_running} for container in containers]

    return items


def get_container_from_id(client, container_id):
    """
    return the docker container from a given id
    """
    return Container.from_id(client, container_id)

def get_volumes(container):
    """
    retrieve container volumes details
    """
    mounts = container.get('Mounts')
    return [dict(source=mount['Source'], destination=mount['Destination']) for mount in mounts]


def get_yml_path(path):
    """
    get path of docker-compose.yml file
    """
    return get_default_config_files(path)[0]

def get_project(path):
    """
    get docker project given file path
    """
    logging.debug('get project ' + path)

    environment = Environment.from_env_file(path)
    config_path = get_config_path_from_options(path, dict(), environment)
    project = compose_get_project(path, config_path)
    return project

def containers():
    """
    active containers
    """
    version = API_VERSIONS[V2_0]
    client = docker_client(Environment(), version)
    return client.containers()
