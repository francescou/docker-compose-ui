from flask import Flask, jsonify, request
from scripts.bridge import ps, get_project
from scripts.find_yml import find_yml_files
from json import loads
import logging
import os

# Flask Application
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path='')

# load project definitions
projects = find_yml_files('/opt/definitions')
logging.debug(projects)

# REST endpoints
@app.route("/api/containers", methods=['GET'])
def containers():
      return jsonify(compose=projects)

@app.route("/api/containers/<name>", methods=['GET'])
def container(name):
    path = projects[name]
    logging.debug('ps ' + path)
    project = get_project(path)
    container = ps(project)
    return jsonify(info=container)

@app.route("/api/logs/<name>", defaults={'limit': "all"}, methods=['GET'])
@app.route("/api/logs/<name>/<int:limit>", methods=['GET'])
def logs(name, limit):
    path = projects[name]
    logging.debug('logs ' + path)
    project = get_project(path)

    logs = {}

    for k in project.containers(stopped=True):
        logging.debug(k.name)
        logging.debug(limit)
        logs[k.name] = k.logs(timestamps=True, tail=limit).split('\n')

    return jsonify(logs=logs)

@app.route("/api/containers/<name>", methods=['DELETE'])
def kill(name):
    logging.debug('kill ' + name)
    path = projects[name]
    project = get_project(path)
    outcome = project.kill()
    return jsonify(info=outcome)

@app.route("/api/containers", methods=['PUT'])
def update():
    j = loads(request.data)
    name = j["id"]
    logging.debug('pull ' + name)
    path = projects[name]
    project = get_project(path)
    outcome = project.pull()
    return jsonify(info=outcome)

@app.route("/api/containers", methods=['POST'])
def up():
    j = loads(request.data)
    name = j["id"]
    logging.debug('up ' + name)
    path = projects[name]
    project = get_project(path)
    logging.debug(project)
    outcome = project.up()
    logging.debug(outcome)
    return jsonify(info=len(outcome))

# static resources
@app.route("/")
def index():
  return app.send_static_file('app/index.html')

# run app
if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True, threaded=True)