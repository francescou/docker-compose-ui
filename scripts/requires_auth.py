"""
Authentication module
inspired by http://flask.pocoo.org/snippets/8/
"""

from functools import wraps
import os
from flask import request, Response

def authentication_enabled():
    """
    check if authentication is enabled
    """
    return 'COMPOSE_USERNAME' in os.environ and 'COMPOSE_PASSWORD' in os.environ
    
def disable_authentication():
    """
    disable authentication
    """
    del os.environ['COMPOSE_USERNAME']
    del os.environ['COMPOSE_PASSWORD']

def set_authentication(username, password):
    """
    enable basic authentication with (username, password)
    """
    os.environ['COMPOSE_USERNAME'] = username
    os.environ['COMPOSE_PASSWORD'] = password

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

def requires_auth(func):
    """
    requires_auth annotation
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        decorator
        """
        auth = request.authorization
        if not authentication_enabled() or (auth and check_auth(auth.username, auth.password)):
            return func(*args, **kwargs)
        return authenticate()
    return decorated
