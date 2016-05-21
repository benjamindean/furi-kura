import os
import sys
from functools import wraps


def get_file(path):
    project_path = os.path.abspath(path)
    user_path = "/usr/share/%s" % path
    return project_path if os.path.isfile(project_path) else user_path


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


def check_lock():
    lockfile = os.path.expanduser('~/.config/furikura/furikura.lock')

    if os.path.isfile(lockfile):
        with open(lockfile, "r") as pidfile:
            if os.path.exists("/proc/%s" % pidfile.readline()):
                sys.exit(1)
            else:
                os.remove(lockfile)
    else:
        os.makedirs(os.path.dirname(lockfile), exist_ok=True)

    with open(lockfile, "w") as lockfile:
        lockfile.write("%s" % os.getpid())
