"""
Authentication module
inspired by http://flask.pocoo.org/snippets/8/
"""

from functools import wraps
import os
from flask import request, Response

def full_authentication_enabled():
    """
    check if full_authentication is enabled
    """
    return os.environ.has_key('COMPOSE_USERNAME_FULL') and os.environ.has_key('COMPOSE_PASSWORD_FULL')

def disable_full_authentication():
    """
    disable full_authentication
    """
    del os.environ['COMPOSE_USERNAME_FULL']
    del os.environ['COMPOSE_PASSWORD_FULL']

def set_full_authentication(username, password):
    """
    enable basic full_authentication with (username, password)
    """
    os.environ['COMPOSE_USERNAME_FULL'] = username
    os.environ['COMPOSE_PASSWORD_FULL'] = password

def check_full_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return os.getenv('COMPOSE_USERNAME_FULL') == username and os.getenv('COMPOSE_PASSWORD_FULL') == password

def full_authenticate():
    """Sends a 401 response that enables basic full_auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="docker-compose-ui"'})

def requires_full_auth(func):
    """
    requires_full_auth annotation
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        """
        decorator
        """
        full_auth = request.authorization
        if not full_authentication_enabled() or (full_auth and check_full_auth(full_auth.username, full_auth.password)):
            return func(*args, **kwargs)
        return full_authenticate()
    return decorated
