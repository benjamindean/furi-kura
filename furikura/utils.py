from os.path import abspath
from os.path import isfile
from functools import wraps

def get_file(path):
    project_path = abspath(path)
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
        result = func(self, *args, **kwargs)
        style = '\033[95m{0}\033[0m'
        print(
            style.format('FUNCTION:'), func.__name__,
            style.format('RESULT:'), result,
            style.format('ARGS:'), *args, **kwargs
        )
        return result
    return wrapper