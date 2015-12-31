from composeui import app
from main import API_V1
from scripts.requires_auth import requires_auth
import os
from flask import jsonify

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