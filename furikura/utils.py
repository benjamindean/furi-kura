import gi
gi.require_version('Gdk', '3.0')

import os
import sys
from functools import wraps
from gi.repository import Gdk as gdk


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


def autostart(action):
    """
    Symlink desktop file to ~/.config/autostart
    """
    autostart = os.path.expanduser('~/.config/autostart/furikura.desktop')
    desktop_file = '/usr/share/applications/furikura.desktop'
    is_enabled = os.path.isfile(autostart)

    if not os.path.isfile(desktop_file):
        return

    if action is 'add' and not is_enabled:
        os.symlink(desktop_file, autostart)
    elif action is 'remove' and is_enabled:
        os.remove(autostart)


"""
The following implementation of getting GTK theme luminance
were stolen from Vagrant Application Indicator (https://github.com/candidtim/vagrant-appindicator)
created by Timur Rubeko (https://github.com/candidtim) because I was too stupid to google RGB Luminance formula.
"""


def __luminance(r, g, b, base=256):
    """Calculates luminance of a color, on a scale from 0 to 1, meaning that 1 is the highest luminance.
    r, g, b arguments values should be in 0..256 limits, or base argument should define the upper limit otherwise"""
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / base


def __pixel_at(x, y):
    """Returns (r, g, b) color code for a pixel with given coordinates (each value is in 0..256 limits)"""
    root_window = gdk.get_default_root_window()
    buf = gdk.pixbuf_get_from_window(root_window, x, y, 1, 1)
    pixels = buf.get_pixels()
    if type(pixels) == type(""):
        rgb = tuple([int(byte.encode('hex'), 16) for byte in pixels])
    else:
        rgb = tuple(pixels)
    return rgb


def get_theme():
    """Returns one of THEME_LIGHT or THEME_DARK, corresponding to current user's UI theme"""
    # getting color of a pixel on a top bar, and identifying best-fitting color theme based on its luminance
    pixel_rgb = __pixel_at(2, 2)
    luminance = __luminance(*pixel_rgb)
    return 'dark' if luminance >= 0.5 else 'light'
