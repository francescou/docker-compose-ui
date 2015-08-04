"""
bridge to docker-compose
"""

from compose.cli.main import TopLevelCommand
from compose.container import Container

import logging

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
        'ports': container.ports,
        'volumes': get_volumes(get_container_from_id(project.client, container.id)),
        'is_running': container.is_running}, containers)

    return items

def get_container_logs(project, container_id, limit):
    """
    get container logs
    """
    container = get_container_from_id(project.client, container_id)
    return container.logs(timestamps=True, tail=limit).split('\n')

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
    config_volumes = container.get('Config.Volumes')
    volumes_rw = container.get('VolumesRW')

    filtered_volumes = filter(lambda volume: not volume in config_volumes, volumes)
    items = map(lambda volume: \
        dict(write=volumes_rw[volume], dest=volume, src=volumes[volume]), \
        filtered_volumes)

    return items

def get_project(path):
    """
    get docker project given file path
    """
    logging.debug('get project ' + path)
    command = TopLevelCommand()
    command.base_dir = path
    project = command.get_project(command.get_config_path())
    return project
