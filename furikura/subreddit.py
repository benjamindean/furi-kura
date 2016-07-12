import gi
import html
import webbrowser
from .utils import get_file

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SubredditChooser(object):
    """
    Separate window for choosing subreddit
    to show inside indicators menu
    """
    def __init__(self, indicator):
        # Passing indicator class and create Gtk.Builder()
        self.indicator = indicator
        self.builder = Gtk.Builder()
        self.chooser = None

    def show_window(self, *args):
        # Getting Entry, Button and ComboBoxText objects
        self.builder.add_from_file(get_file('furikura/ui/subreddit.xml'))
        self.chooser = self.builder.get_object('choose_subreddit')

        subreddit_name = self.builder.get_object('subreddit_name')
        posts_type = self.builder.get_object('posts_type')
        posts_limit = self.builder.get_object('posts_limit')
        use_permalink = self.builder.get_object('use_permalink')

        save = self.builder.get_object('save')
        cancel = self.builder.get_object('cancel')

        # Setting previously saved values
        subreddit_name.set_text(self.indicator.config.get('subreddit', ''))
        posts_type.set_active_id(self.indicator.config.get('posts_type', '1'))
        posts_limit.set_active_id(self.indicator.config.get('posts_limit', '5'))
        use_permalink.set_active(self.indicator.config.get('use_permalink', False))

        # Connecting event handlers
        cancel.connect('clicked', self.__chooser_destroy)
        save.connect('clicked', self.__chooser_save, (subreddit_name, posts_type, posts_limit, use_permalink))

        # Show the window
        self.chooser.set_position(Gtk.WindowPosition(1))
        self.chooser.show()

    def update_indicator(self):
        # Get subreddit name from config
        subreddit = self.indicator.config.get('subreddit')

        # Exit if not specified
        if not subreddit:
            return

        posts_type = self.indicator.config.get('posts_type', 1)
        posts_limit = self.indicator.config.get('posts_limit', '5')

        types = {
            1: 'new',
            2: 'hot',
            3: 'top',
            4: 'random'
        }

        type_string = types[int(posts_type)]

        # Get last posts
        data = self.indicator.request.get_subreddit(subreddit, type_string, posts_limit)

        # Exit if not specified
        if not data:
            return

        # Where to append
        menu = self.indicator.builder.get_object('furikura_menu')

        for child in menu.get_children():
            if child.get_name() == 'subreddit_post':
                child.destroy()

        # Show title
        name = self.indicator.builder.get_object('subreddit')
        name.set_label('/r/%s/%s' % (subreddit, type_string))
        name.show()

        # Show separator
        self.indicator.builder.get_object('subreddit_separator_one').show()
        self.indicator.builder.get_object('subreddit_separator_two').show()

        # Iterate through last posts and append them to the menu
        for post in data:
            title = post['title'][:40] + (post['title'][40:] and '...')
            item = Gtk.MenuItem('{upvotes}{gold} |  {title}'.format(
                upvotes=post['upvotes'],
                gold=' \u2605' if post['gilded'] else '',
                title=html.unescape(title)
            ))
            url = 'https://www.reddit.com' + post['permalink'] \
                if self.indicator.config.get('use_permalink') \
                else post['link']
            item.connect('activate', self.__open_url, url)
            item.set_name('subreddit_post')
            menu.add_child(self.indicator.builder, item)
            item.show()

    def __open_url(self, widget, link):
        webbrowser.open(link, new=1, autoraise=True)

    def __chooser_destroy(self, *args):
        """
        Wrapper for .destroy() method
        """
        self.chooser.destroy()

    def __chooser_save(self, widget, data):
        # Getting text and id values
        cfg_options = {
            'subreddit': data[0].get_text(),
            'posts_type': data[1].get_active_id(),
            'posts_limit': data[2].get_active_id(),
            'use_permalink': data[3].get_active()
        }

        # Store everything is config
        for key, value in cfg_options.items():
            self.indicator.cfg_cls.set_key(key, value)

        # Destroy the window after saving config
        self.indicator.subreddit_updates()
        self.__chooser_destroy()
