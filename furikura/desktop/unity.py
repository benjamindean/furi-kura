import gi
from threading import Timer

gi.require_version('Unity', '7.0')
from gi.repository import Unity, Dbusmenu


launcher = Unity.LauncherEntry.get_for_desktop_id("furikura.desktop")

def update_counter(count):
    launcher.set_property("count", count)
    launcher.set_property("count_visible", True)

    if count > 0:
        launcher.set_property("urgent", True)
        timer = Timer(3, launcher.set_property, ['urgent', False])
        timer.start()

def add_quicklist_item(item):
    quick_list = Dbusmenu.Menuitem.new()
    list_item = Dbusmenu.Menuitem.new()
    list_item.property_set(Dbusmenu.MENUITEM_PROP_LABEL, item)
    list_item.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, True)
    quick_list.child_append(list_item)
    launcher.set_property("quicklist", quick_list)