from git import Repo
import os
import logging
from scripts.find_yml import YML_PATH

git_repo = os.getenv('GIT_REPO')

if git_repo:
  YML_PATH = YML_PATH + '-git'

logging.basicConfig(level=logging.DEBUG)

def git_pull():
    if git_repo:
      logging.info('git pull ' + git_repo)
      Repo(YML_PATH).remote('origin').pull()
    else:
      logging.info('will not execute git pull: not a git repository')

if git_repo:
    logging.info('git repo: ' + git_repo)
    if os.path.isdir(os.path.join(YML_PATH, '.git')):
        git_pull()
    else:
        logging.info('git clone ' +  git_repo)
        Repo.clone_from(git_repo, YML_PATH)