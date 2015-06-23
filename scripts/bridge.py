"""
bridge to docker-compose
"""

from compose.cli.main import TopLevelCommand
import logging

def ps_(project):
    """
    containers status
    """
    logging.debug('ps ' + project.name)
    containers = project.containers(stopped=True) + project.containers(one_off=True)
    items = map(lambda container: {
        'name': container.name,
        'command': container.human_readable_command,
        'state': container.human_readable_state,
        'ports': container.ports,
        'is_running': container.is_running}, containers)

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
