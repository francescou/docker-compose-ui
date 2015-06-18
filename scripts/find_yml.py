"""
find docker-compose.yml files
"""

import fnmatch
import os

def find_yml_files(path):
    """
    find docker-compose.yml files in path
    """
    matches = {}
    for root, _, filenames in os.walk(path):
        for _ in fnmatch.filter(filenames, 'docker-compose.yml'):
            key = root.split('/')[-1]
            matches[key] = os.path.join(os.getcwd(), root)
    return matches
