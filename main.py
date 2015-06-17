"""
Docker Compose UI, flask based application
"""

from flask import Flask, jsonify, request
from scripts.bridge import ps_, get_project
from scripts.find_yml import find_yml_files
from json import loads
import logging

# Flask Application
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path='')

# load project definitions
projects = find_yml_files('/opt/definitions')
logging.debug(projects)

def get_project_with_name(name):
    """
    get docker compose project given a project name
    """
    path = projects[name]
    return get_project(path)

# REST endpoints

@app.route("/api/containers", methods=['GET'])
def containers():
    """
    List docker compose projects
    """
    return jsonify(compose=projects)

@app.route("/api/containers/<name>", methods=['GET'])
def container(name):
    """
    get project details
    """
    project = get_project_with_name(name)
    the_container = ps_(project)
    return jsonify(info=the_container)

@app.route("/api/logs/<name>", defaults={'limit': "all"}, methods=['GET'])
@app.route("/api/logs/<name>/<int:limit>", methods=['GET'])
def logs(name, limit):
    """
    docker-compose logs
    """
    lines = {}
    for k in get_project_with_name(name).containers(stopped=True):
        lines[k.name] = k.logs(timestamps=True, tail=limit).split('\n')

    return jsonify(logs=lines)

@app.route("/api/containers/<name>", methods=['DELETE'])
def kill(name):
    """
    docker-compose kill
    """
    outcome = get_project_with_name(name).kill()
    return jsonify(info=outcome)

@app.route("/api/containers", methods=['PUT'])
def pull():
    """
    docker-compose pull
    """
    name = loads(request.data)["id"]
    outcome = get_project_with_name(name).pull()
    return jsonify(info=outcome)

@app.route("/api/containers", methods=['POST'])
def up_():
    """
    docker-compose up
    """
    name = loads(request.data)["id"]
    outcome = get_project_with_name(name).up()
    logging.debug(outcome)
    return jsonify(info=len(outcome))

# static resources
@app.route("/")
def index():
    """
    index.html
    """
    return app.send_static_file('app/index.html')

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
