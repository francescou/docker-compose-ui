"""
bridge to docker-compose
"""

import logging
import os
import codecs
import six
from compose.container import Container
from compose.cli.command import get_project as compose_get_project, get_config_path_from_options
from compose.config.config import get_default_config_files
from compose.config.environment import Environment

from compose.cli.docker_client import docker_client
from compose.const import API_VERSIONS
from compose.config.config import V2_0

def split_env(env):
    if isinstance(env, six.binary_type):
        env = env.decode('utf-8', 'replace')
    if '=' in env:
        return env.split('=', 1)
    else:
        return env, None

def env_vars_from_file(filename):
    """
    Read in a line delimited file of environment variables.
    """
    env = {}
    if not os.path.exists(filename):
        return env
    elif not os.path.isfile(filename):
        return env
    for line in codecs.open(filename, 'r', 'utf-8'):
        line = line.strip()
        if line and not line.startswith('#'):
            k, v = split_env(line)
            env[k] = v
    return env


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
    apply env var for docker-compose.yml substitutions
    """
    globalenv = env_vars_from_file(path + "/../compose-projects.env")
    localenv = env_vars_from_file(path + "/.env")
    localenv.update(globalenv)
    for key, value in localenv.iteritems():
        logging.debug('environment: ' + key + ' ' + value)
        os.environ[key] = value

    """
    get docker project given file path
    add locale env car defined in file path/.env to docker-compose then cleanup
    """
    logging.debug('get project ' + path)
    environment = Environment.from_env_file(path)


    config_path = get_config_path_from_options(path, dict(), environment)
    project = compose_get_project(path, config_path)

    """ 
    clean-up locale env var
    """
    for key, value in localenv.iteritems():
        logging.debug('cleanup: ' + key + ' ' + value)
        del os.environ[key]

    return project

def containers():
    """
    active containers
    """
    version = API_VERSIONS[V2_0]
    client = docker_client(Environment(), version)
    return client.containers()
