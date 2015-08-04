"""
Docker Compose UI, flask based application
"""

from flask import Flask, jsonify, request
from scripts.bridge import ps_, get_project, get_container_from_id
from scripts.find_yml import find_yml_files
from scripts.requires_auth import requires_auth, authentication_enabled, disable_authentication, set_authentication
from json import loads
import logging
import requests
import docker
import os

# Flask Application
API_V1 = '/api/v1/'
YML_PATH = '/opt/docker-compose-projects'
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path='')

# load project definitions
projects = find_yml_files(YML_PATH)

logging.debug(projects)


def get_project_with_name(name):
    """
    get docker compose project given a project name
    """
    path = projects[name]
    return get_project(path)

# REST endpoints

@app.route(API_V1 + "projects", methods=['GET'])
def list_projects():
    """
    List docker compose projects
    """
    global projects
    projects = find_yml_files(YML_PATH)
    return jsonify(projects=projects)

@app.route(API_V1 + "projects/<name>", methods=['GET'])
def project_containers(name):
    """
    get project details
    """
    project = get_project_with_name(name)
    containers = ps_(project)
    return jsonify(containers=containers)


@app.route(API_V1 + "projects/<name>/<container_id>", methods=['GET'])
def project_container(name, container_id):
    """
    get container details
    """
    project = get_project_with_name(name)
    container = get_container_from_id(project.client, container_id)
    return jsonify(
        id=container.id,
        short_id=container.short_id,
        human_readable_command=container.human_readable_command,
        name=container.name,
        number=container.number,
        ports=container.ports,
        labels=container.labels,
        log_config=container.log_config,
        image=container.image,
        links=container.links(),
        environment=container.environment
        )

@app.route(API_V1 + "projects/<name>", methods=['DELETE'])
@requires_auth
def kill(name):
    """
    docker-compose kill
    """
    get_project_with_name(name).kill()
    return jsonify(command='kill')

@app.route(API_V1 + "projects", methods=['PUT'])
@requires_auth
def pull():
    """
    docker-compose pull
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).pull()
    return jsonify(command='pull')

@app.route(API_V1 + "projects", methods=['POST'])
@requires_auth
def up_():
    """
    docker-compose up
    """
    name = loads(request.data)["id"]
    containers = get_project_with_name(name).up()
    logging.debug(containers)
    return jsonify(
        {
            'command': 'up',
            'containers': map(lambda container: container.name, containers)
        })

@app.route(API_V1 + "build", methods=['POST'])
@requires_auth
def build():
    """
    docker-compose build
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).build()
    return jsonify(command='build')

@app.route(API_V1 + "logs/<name>", defaults={'limit': "all"}, methods=['GET'])
@app.route(API_V1 + "logs/<name>/<int:limit>", methods=['GET'])
def logs(name, limit):
    """
    docker-compose logs
    """
    lines = {}
    for k in get_project_with_name(name).containers(stopped=True):
        lines[k.name] = k.logs(timestamps=True, tail=limit).split('\n')

    return jsonify(logs=lines)

@app.route(API_V1 + "logs/<name>/<container_id>", defaults={'limit': "all"}, methods=['GET'])
@app.route(API_V1 + "logs/<name>/<container_id>/<int:limit>", methods=['GET'])
def container_logs(name, container_id, limit):
    """
    docker-compose logs of a specific container
    """
    project = get_project_with_name(name)
    container = get_container_from_id(project.client, container_id)
    lines = container.logs(timestamps=True, tail=limit).split('\n')
    return jsonify(logs=lines)

@app.route(API_V1 + "host", methods=['GET'])
def host():
    """
    docker host info
    """
    host = os.getenv('DOCKER_HOST')

    return jsonify(host=host)


@app.route(API_V1 + "host", methods=['POST'])
@requires_auth
def set_host():
    """
    set docker host
    """
    new_host = loads(request.data)["id"]
    if new_host == None:
        if os.environ.has_key('DOCKER_HOST'):
            del os.environ['DOCKER_HOST']
        return jsonify()
    else:
        os.environ['DOCKER_HOST'] = new_host
        return jsonify(host=new_host)

@app.route(API_V1 + "authentication", methods=['GET'])
def authentication():
    """
    check if basic authentication is enabled
    """
    return jsonify(enabled=authentication_enabled())

@app.route(API_V1 + "authentication", methods=['DELETE'])
@requires_auth
def disable_basic_authentication():
    """
    disable basic authentication
    """
    disable_authentication()
    return jsonify(enabled=False)

@app.route(API_V1 + "authentication", methods=['POST'])
@requires_auth
def enable_basic_authentication():
    """
    set up basic authentication
    """
    data = loads(request.data)
    set_authentication(data["username"], data["password"])
    return jsonify(enabled=True)

# static resources
@app.route("/")
def index():
    """
    index.html
    """
    return app.send_static_file('index.html')

## basic exception handling

@app.errorhandler(requests.exceptions.ConnectionError)
def handle_connection_error(err):
    """
    connection exception handler
    """
    return 'docker host not found: ' + str(err), 500

@app.errorhandler(docker.errors.DockerException)
def handle_docker_error(err):
    """
    docker exception handler
    """
    return 'docker exception: ' + str(err), 500

@app.errorhandler(Exception)
def handle_generic_error(err):
    """
    default exception handler
    """
    return 'error: ' + str(err), 500

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
