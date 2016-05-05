import os.path
from os.path import isfile


def get_file(path):
    project_path = os.path.abspath(path)
    user_path = "/usr/share/%s" % path
    return project_path if isfile(project_path) else user_path
