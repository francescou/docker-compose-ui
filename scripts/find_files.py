"""
find docker-compose.yml files
"""
import fnmatch
import re
import os

def find_yml_files(path):
    """
    find docker-compose.yml files in path
    """
    matches = {}
    for root, _, filenames in os.walk(path):
        for file_name in fnmatch.filter(filenames, 'docker-compose*.yml'):
            key = root.split('/')[-1]
            path = os.path.join(os.getcwd(), root)
            m = re.search('docker-compose(.+).yml', file_name)
            if m == None:
                matches[key] = path
            else:
                matches[key + m.group(1)] = path
    return matches


def get_readme_file(path):
    """
    find case insensitive readme.md in path and return the contents
    """

    readme = None

    for file in os.listdir(path):
        if file.lower() == "readme.md" and os.path.isfile(os.path.join(path, file)):
            file = open(os.path.join(path, file))
            readme = file.read()
            file.close()
            break

    return readme

def get_logo_file(path):
    """
    find case insensitive logo.png in path and return the contents
    """

    logo = None

    for file in os.listdir(path):
        if file.lower() == "logo.png" and os.path.isfile(os.path.join(path, file)):
            file = open(os.path.join(path, file))
            logo = file.read()
            file.close()
            break

    return logo
