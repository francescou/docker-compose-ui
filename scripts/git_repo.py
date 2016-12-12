"""
git functionalities
"""

import os
import logging
from git import Repo

git_repo = os.getenv('GIT_REPO')

logging.basicConfig(level=logging.DEBUG)

GIT_YML_PATH = '/opt/docker-compose-projects-git/'

def git_pull():
    """
    perform git pull
    """
    if git_repo:
        logging.info('git pull ' + git_repo)
        Repo(GIT_YML_PATH).remote('origin').pull()
    else:
        logging.info('will not execute git pull: not a git repository')

if git_repo:
    logging.info('git repo: ' + git_repo)
    if os.path.isdir(os.path.join(GIT_YML_PATH, '.git')):
        git_pull()
    else:
        logging.info('git clone ' +  git_repo)
        Repo.clone_from(git_repo, GIT_YML_PATH)
