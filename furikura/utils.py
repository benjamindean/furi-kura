import os.path
from os.path import isfile
from functools import wraps

def get_file(path):
    project_path = os.path.abspath(path)
    user_path = "/usr/share/%s" % path
    return project_path if isfile(project_path) else user_path

def check_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False

    return wrapper

def debug(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(func.__name__, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper