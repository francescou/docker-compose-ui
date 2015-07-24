# inspired by http://flask.pocoo.org/snippets/8/

from functools import wraps
from flask import request, Response
import os

def authentication_disabled():
    return os.environ.has_key('COMPOSE_USERNAME') is None or os.environ.has_key('COMPOSE_PASSWORD') is None

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return os.getenv('COMPOSE_USERNAME') == username and os.getenv('COMPOSE_PASSWORD') == password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="docker-compose-ui"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if authentication_disabled() or (auth and check_auth(auth.username, auth.password)):
            return f(*args, **kwargs)
        return authenticate()
    return decorated
