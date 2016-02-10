"""
Docker Compose UI, flask based application
"""

from compose.service import ImageType
from json import loads
import logging
import os
import traceback
import docker
import requests
from flask import Flask, jsonify, request
from scripts.bridge import ps_, get_project, get_container_from_id, get_yml_path
from scripts.find_yml import find_yml_files
from scripts.requires_auth import requires_auth, authentication_enabled, \
  disable_authentication, set_authentication

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

@app.route(API_V1 + "projects/<project>/<service_id>", methods=['POST'])
@requires_auth
def run_service(project, service_id):
    """
    docker-compose run service
    """
    json = loads(request.data)
    service = get_project_with_name(project).get_service(service_id)

    command = json["command"] if 'command' in json else service.options.get('command')

    container = service \
        .create_container(one_off=True, command=command)
    container.start()

    return jsonify(\
        command='run %s/%s' % (project, service_id), \
        name=container.name, \
        id=container.id \
        )

@app.route(API_V1 + "projects/yml/<name>", methods=['GET'])
def project_yml(name):
    """
    get yml content
    """
    path = get_yml_path(projects[name])
    with open(path) as data_file:
        return jsonify(yml=data_file.read())

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
        name_without_project=container.name_without_project,
        number=container.number,
        ports=container.ports,
        ip=container.get('NetworkSettings.IPAddress'),
        labels=container.labels,
        log_config=container.log_config,
        image=container.image,
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

@app.route(API_V1 + "services", methods=['PUT'])
@requires_auth
def scale():
    """
    docker-compose scale
    """
    req = loads(request.data)
    name = req['project']
    service_name = req['service']
    num = req['num']

    project = get_project_with_name(name)
    project.get_service(service_name).scale(desired_num=int(num))
    return jsonify(command='scale')

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
    json = loads(request.data)
    name = json["id"]

    dic = dict(no_cache=json["no_cache"] if "no_cache" in json \
      else None, pull=json["pull"] if "pull" in json else None)

    get_project_with_name(name).build(**dic)

    return jsonify(command='build')

@app.route(API_V1 + "create", methods=['POST'])
@requires_auth
def create():
    """
    create new project
    """
    data = loads(request.data)

    directory = YML_PATH + '/' + data["name"]
    os.makedirs(directory)

    file_path = directory + "/docker-compose.yml"
    out_file = open(file_path, "w")
    out_file.write(data["yml"])
    out_file.close()

    return jsonify(path=file_path)


@app.route(API_V1 + "search", methods=['POST'])
def search():
    """
    search for a project on www.composeregistry.com
    """
    query = loads(request.data)['query']
    response = requests.get('https://www.composeregistry.com/api/v1/search', \
        params={'query': query}, headers={'x-key': 'default'})
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        result = jsonify(response.json())
        result.status_code = response.status_code
        return result


@app.route(API_V1 + "yml", methods=['POST'])
def yml():
    """
    get yml content from www.composeregistry.com
    """
    item_id = loads(request.data)['id']
    response = requests.get('https://www.composeregistry.com/api/v1/yml', \
        params={'id': item_id}, headers={'x-key': 'default'})
    return jsonify(response.json())


@app.route(API_V1 + "start", methods=['POST'])
@requires_auth
def start():
    """
    docker-compose start
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).start()
    return jsonify(command='start')

@app.route(API_V1 + "stop", methods=['POST'])
@requires_auth
def stop():
    """
    docker-compose stop
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).stop()
    return jsonify(command='stop')

@app.route(API_V1 + "down", methods=['POST'])
@requires_auth
def down():
    """
    docker-compose down
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).down(ImageType.none, None)
    return jsonify(command='down')

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
    host_value = os.getenv('DOCKER_HOST')

    return jsonify(host=host_value)


@app.route(API_V1 + "host", methods=['POST'])
@requires_auth
def set_host():
    """
    set docker host
    """
    new_host = loads(request.data)["id"]
    if new_host is None:
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
    traceback.print_exc()
    return 'error: ' + str(err), 500

# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
