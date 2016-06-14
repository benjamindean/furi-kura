import gi

gi.require_version('Unity', '7.0')
from gi.repository import Unity


def update_counter(count):
    launcher = Unity.LauncherEntry.get_for_desktop_id("furikura.desktop")
    launcher.set_property("count", count)
    launcher.set_property("count_visible", True)
