"""
find docker-compose.yml files
"""

import fnmatch
import os

YML_PATH = '/opt/docker-compose-projects'

def find_yml_files():
    """
    find docker-compose.yml files in path
    """
    matches = {}
    for root, _, filenames in os.walk(YML_PATH):
        for _ in fnmatch.filter(filenames, 'docker-compose.yml'):
            key = root.split('/')[-1]
            matches[key] = os.path.join(os.getcwd(), root)
    return matches
