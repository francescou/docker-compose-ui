import fnmatch
import os

def find_yml_files(path):
  matches = {}
  for root, dirnames, filenames in os.walk(path):
    for filename in fnmatch.filter(filenames, '*.yml'):
      key = root[len(path) + 1:]
      matches[key] = os.path.join(os.getcwd(), root)
  return matches
