"""
Docker Compose UI, flask based application
"""

from json import loads
import logging
import os
import traceback
from shutil import rmtree
from compose.service import ImageType, BuildAction
import docker
import requests
from flask import Flask, jsonify, request, abort
from scripts.git_repo import git_pull, git_repo, GIT_YML_PATH
from scripts.bridge import ps_, get_project, get_container_from_id, get_yml_path, containers, project_config, info
from scripts.find_files import find_yml_files, get_readme_file, get_logo_file
from scripts.requires_auth import requires_auth, authentication_enabled, \
  disable_authentication, set_authentication
from scripts.manage_project import manage

# Flask Application
API_V1 = '/api/v1/'
YML_PATH = os.getenv('DOCKER_COMPOSE_UI_YML_PATH') or '.'
COMPOSE_REGISTRY = os.getenv('DOCKER_COMPOSE_REGISTRY')

logging.basicConfig(level=logging.INFO)
app = Flask(__name__, static_url_path='')

def load_projects():
    """
    load project definitions (docker-compose.yml files)
    """
    global projects

    if git_repo:
        git_pull()
        projects = find_yml_files(GIT_YML_PATH)
    else:
        projects = find_yml_files(YML_PATH)

    logging.info(projects)

load_projects()


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
    load_projects()
    active = [container['Labels']['com.docker.compose.project'] \
        if 'com.docker.compose.project' in container['Labels'] \
        else [] for container in containers()]
    return jsonify(projects=projects, active=active)

@app.route(API_V1 + "remove/<name>", methods=['DELETE'])
@requires_auth
def rm_(name):
    """
    remove previous cached containers. docker-compose rm -f
    """
    project = get_project_with_name(name)
    project.remove_stopped()
    return jsonify(command='rm')

@app.route(API_V1 + "projects/<name>", methods=['GET'])
def project_containers(name):
    """
    get project details
    """
    project = get_project_with_name(name)
    return jsonify(containers=ps_(project))

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
    folder_path = projects[name]
    path = get_yml_path(folder_path)
    config = project_config(folder_path)

    with open(path) as data_file:
        env = None
        if os.path.isfile(folder_path + '/.env'):
            with open(folder_path + '/.env') as env_file:
                env = env_file.read()

        return jsonify(yml=data_file.read(), env=env, config=config._replace(config_version=config.config_version.__str__(), version=config.version.__str__()))



@app.route(API_V1 + "projects/readme/<name>", methods=['GET'])
def get_project_readme(name):
    """
    get README.md or readme.md if available
    """
    path = projects[name]
    return jsonify(readme=get_readme_file(path))

@app.route(API_V1 + "projects/logo/<name>", methods=['GET'])
def get_project_logo(name):
    """
    get logo.png if available
    """
    path = projects[name]
    logo = get_logo_file(path)
    if logo is None:
        abort(404)
    return logo


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
        environment=container.environment,
        started_at=container.get('State.StartedAt'),
        repo_tags=container.image_config['RepoTags']
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
    req = loads(request.data)
    name = req["id"]
    service_names = req.get('service_names', None)
    do_build = BuildAction.force if req.get('do_build', False) else BuildAction.none

    container_list = get_project_with_name(name).up(
        service_names=service_names,
        do_build=do_build)

    return jsonify(
        {
            'command': 'up',
            'containers': [container.name for container in container_list]
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

@app.route(API_V1 + "create-project", methods=['POST'])
@app.route(API_V1 + "create", methods=['POST'])
@requires_auth
def create_project():
    """
    create new project
    """
    data = loads(request.data)

    file_path = manage(YML_PATH + '/' +  data["name"], data["yml"], False)

    if 'env' in data and data["env"]:
        env_file = open(YML_PATH + '/' + data["name"] + "/.env", "w")
        env_file.write(data["env"])
        env_file.close()

    load_projects()

    return jsonify(path=file_path)


@app.route(API_V1 + "update-project", methods=['PUT'])
@requires_auth
def update_project():
    """
    update project
    """
    data = loads(request.data)
    file_path = manage(YML_PATH + '/' +  data["name"], data["yml"], True)

    if 'env' in data and data["env"]:
        env_file = open(YML_PATH + '/' + data["name"] + "/.env", "w")
        env_file.write(data["env"])
        env_file.close()

    return jsonify(path=file_path)


@app.route(API_V1 + "remove-project/<name>", methods=['DELETE'])
@requires_auth
def remove_project(name):
    """
    remove project
    """

    directory = YML_PATH + '/' + name
    rmtree(directory)
    load_projects()
    return jsonify(path=directory)


@app.route(API_V1 + "search", methods=['POST'])
def search():
    """
    search for a project on a docker-compose registry 
    """
    query = loads(request.data)['query']
    response = requests.get(COMPOSE_REGISTRY + '/api/v1/search', \
        params={'query': query}, headers={'x-key': 'default'})
    result = jsonify(response.json())
    if response.status_code != 200:
        result.status_code = response.status_code
    return result


@app.route(API_V1 + "yml", methods=['POST'])
def yml():
    """
    get yml content from a docker-compose registry 
    """
    item_id = loads(request.data)['id']
    response = requests.get(COMPOSE_REGISTRY + '/api/v1/yml', \
        params={'id': item_id}, headers={'x-key': 'default'})
    return jsonify(response.json())


@app.route(API_V1 + "_create", methods=['POST'])
@requires_auth
def create():
    """
    docker-compose create
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).create()
    return jsonify(command='create')

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

@app.route(API_V1 + "restart", methods=['POST'])
@requires_auth
def restart():
    """
    docker-compose restart
    """
    name = loads(request.data)["id"]
    get_project_with_name(name).restart()
    return jsonify(command='restart')

@app.route(API_V1 + "logs/<name>", defaults={'limit': "all"}, methods=['GET'])
@app.route(API_V1 + "logs/<name>/<int:limit>", methods=['GET'])
def logs(name, limit):
    """
    docker-compose logs
    """
    lines = {}
    for k in get_project_with_name(name).containers(stopped=True):
        lines[k.name] = k.logs(timestamps=True, tail=limit).decode().split('\n')
 
    return jsonify(logs=lines)

@app.route(API_V1 + "logs/<name>/<container_id>", defaults={'limit': "all"}, methods=['GET'])
@app.route(API_V1 + "logs/<name>/<container_id>/<int:limit>", methods=['GET'])
def container_logs(name, container_id, limit):
    """
    docker-compose logs of a specific container
    """
    project = get_project_with_name(name)
    container = get_container_from_id(project.client, container_id)
    lines = container.logs(timestamps=True, tail=limit).decode().split('\n')
    return jsonify(logs=lines)

@app.route(API_V1 + "host", methods=['GET'])
def host():
    """
    docker host info
    """
    host_value = os.getenv('DOCKER_HOST')

    return jsonify(host=host_value, workdir=os.getcwd() if YML_PATH == '.' else YML_PATH)

@app.route(API_V1 + "compose-registry", methods=['GET'])
def compose_registry():
    """
    docker compose registry
    """
    return jsonify(url = COMPOSE_REGISTRY)

@app.route(API_V1 + "web_console_pattern", methods=['GET'])
def get_web_console_pattern():
    """
    forward WEB_CONSOLE_PATTERN env var from server to spa
    """
    return jsonify(web_console_pattern=os.getenv('WEB_CONSOLE_PATTERN'))

@app.route(API_V1 + "health", methods=['GET'])
def health():
    """
    docker health
    """
    return jsonify(info())

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
    app.run(host='0.0.0.0', debug=False, threaded=True)
