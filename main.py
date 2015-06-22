"""
Docker Compose UI, flask based application
"""

from flask import Flask, jsonify, request
from scripts.bridge import ps_, get_project
from scripts.find_yml import find_yml_files
from json import loads
import logging
import requests
import docker

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

@app.route(API_V1 + "projects/<name>", methods=['DELETE'])
def kill(name):
    """
    docker-compose kill
    """
    get_project_with_name(name).kill()
    return jsonify(command='kill')

@app.route(API_V1 + "projects", methods=['PUT'])
def pull():
    """
    docker-compose pull
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).pull()
    return jsonify(command='pull')

@app.route(API_V1 + "projects", methods=['POST'])
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
def build():
    """
    docker-compose build
    """
    name = loads(request.data)["id"]
    data = get_project_with_name(name).build()
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

# static resources
@app.route("/")
def index():
    """
    index.html
    """
    return app.send_static_file('index.html')

## basic exception handling

@app.errorhandler(requests.exceptions.ConnectionError)
def handleServerError(e):
    return 'docker host not found: ' + str(e), 500

@app.errorhandler(docker.errors.DockerException)
def handleServerError(e):
    return 'docker exception: ' + str(e), 500

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
