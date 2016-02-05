"""
bridge to docker-compose
"""

import logging
from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options
from compose.config.config import get_default_config_files

def ps_(project):
    """
    containers status
    """
    logging.debug('ps ' + project.name)
    containers = project.containers(stopped=True) + project.containers(one_off=True)

    items = map(lambda container: {
        'name': container.name,
        'name_without_project': container.name_without_project,
        'command': container.human_readable_command,
        'state': container.human_readable_state,
        'labels': container.labels,
        'ports': container.ports,
        'volumes': get_volumes(get_container_from_id(project.client, container.id)),
        'is_running': container.is_running}, containers)

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
    volumes = container.get('Volumes')
    volumes_rw = container.get('VolumesRW')

    items = map(lambda volume: \
        dict(write=volumes_rw[volume], dest=volume, src=volumes[volume]), \
        volumes if volumes else [])

    return items

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
    config_path = get_config_path_from_options(dict([('--file', path)]))
    project = compose_get_project(config_path)
    return project
