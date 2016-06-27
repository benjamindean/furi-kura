import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .utils import get_file


class SubredditChooser(object):

    def __init__(self, config_storage):
        self.config_storage = config_storage
        self.config = self.config_storage.config
        self.builder = Gtk.Builder()
        self.builder.add_from_file(get_file('furikura/ui/subreddit.xml'))
        self.chooser = self.builder.get_object('choose_subreddit')

    def show_window(self):
        self.subreddit_name = self.builder.get_object('subreddit_name')
        self.posts_type = self.builder.get_object('posts_type')

        self.subreddit_name.set_text(self.config.get('subreddit'))
        self.posts_type.set_active(self.config.get('posts_type', 1))

        signals = {
            'chooser_destroy': self.__chooser_destroy,
            'chooser_save': self.__chooser_save
        }

        self.builder.connect_signals(signals)
        self.chooser.show()

    def __chooser_destroy(self, widget):
        self.chooser.destroy()

    def __chooser_save(self, widget):
        self.config_storage.set_key('subreddit', self.subreddit_name.get_text())
        self.config_storage.set_key('posts_type', self.posts_type.get_active())
        self.chooser.destroy()
