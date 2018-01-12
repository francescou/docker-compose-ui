"""
docker compose project management
"""

from os import rename, makedirs, path
from time import time

def manage(directory, yml, is_update):
    """
    create or update docker compose project
    """

    file_path = directory + "/docker-compose.yml" if path.exists(directory + "/docker-compose.yml") else "/docker-compose.yaml"

    if is_update:
        rename(file_path, file_path + "." + str(int(round(time()))))
    else:
        makedirs(directory)

    out_file = open(file_path, "w")
    out_file.write(yml)
    out_file.close()

    return file_path
