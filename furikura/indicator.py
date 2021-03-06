import gi
import os
import webbrowser

from .api import API
from .subreddit import SubredditChooser
from .utils import get_file, get_theme, autostart

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify
from gi.repository import GObject
from gi.repository import GdkPixbuf

if os.environ.get('DESKTOP_SESSION') == 'ubuntu':
    from .desktop import unity as desktop
else:
    from .desktop import default as desktop


class FuriKuraIndicator(object):
    # Init appindicator
    APPINDICATOR_ID = 'furikura_indicator'
    THEME = get_theme()
    ICONS = {
        'active': get_file('furikura/icons/%s/furi-active.png' % THEME),
        'attention': get_file('furikura/icons/%s/furi-attention.png' % THEME),
        'main': get_file('furikura/icons/furi-kura.png')
    }
    INDICATOR = AppIndicator3.Indicator.new(
        APPINDICATOR_ID,
        ICONS['active'],
        AppIndicator3.IndicatorCategory.COMMUNICATIONS
    )

    def __init__(self, cfg_cls):

        # Throwing config class here
        self.cfg_cls = cfg_cls

        # Instantiating API handler
        self.request = API(self.cfg_cls)

        # Getting initial config
        self.config = self.cfg_cls.config

        # Init GTK Builder
        self.builder = Gtk.Builder()

        # Dummy local data
        self.local_data = {
            'inbox_count': 0,
            'comment_karma': 0,
            'link_karma': 0
        }

        # Running services
        self.services = {
            'notification': None,
            'timeout': None
        }

        # Init karma view
        self.karma = '? | ?'

        # Init SubredditChooser window
        self.subreddit_chooser = SubredditChooser(self)

        self.init_appindicator()

    def init_appindicator(self):
        """ Set initial status and attention icon. """
        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.INDICATOR.set_attention_icon(self.ICONS['attention'])

    def update_reddit_data(self):
        """ Update indicator with new data. """
        self.update_appindicator(self.request.get_user_info())
        return True

    """
    Background processing.
    """

    def update_appindicator(self, reddit_data):
        """
        Set all MenuItems to the new values
        and update local copy.
        """
        if reddit_data.get('error'):
            return

        self.set_inbox(reddit_data.get('inbox_count', 0))
        self.mail_notify(reddit_data.get('inbox_count', 0))
        self.set_karma(reddit_data.get('link_karma', 0), reddit_data.get('comment_karma', 0))
        self.local_data = reddit_data
        self.subreddit_updates()

    def run_background(self, interval=1):
        """
        Convert minute interval to seconds
        and updated services with new timeout.
        """
        timeout = interval * 60 * 1000
        self.services['timeout'] = GObject.timeout_add(timeout, self.update_reddit_data)

    def set_refresh_interval(self, widget):
        """
        Set new refresh interval and remove existing
        timeout if already exist.
        """
        interval = int(widget.get_name())
        if interval != self.config.get('refresh_interval'):
            GObject.source_remove(self.services['timeout'])
            self.run_background(interval)
            self.cfg_cls.set_key('refresh_interval', interval)

    """
    Karma handlers.
    """

    def __compare_karma(self, karma_view, karma):
        """
        Return UP or DOWN arrow
        depending on new karma value.
        """
        if not self.local_data.get(karma_view) or not karma:
            return
        if self.local_data.get(karma_view) > karma:
            return '\u2193'
        elif self.local_data.get(karma_view) < karma:
            return '\u2191'

    def set_karma(self, link_karma, comment_karma):
        """
        Format Karma string with new values.
        """
        if link_karma is None or comment_karma is None:
            return
        self.karma = "{link_arrow}{link} | {comment_arrow}{post}".format(
            link=link_karma,
            post=comment_karma,
            link_arrow=self.__compare_karma('link_karma', link_karma) or '',
            comment_arrow=self.__compare_karma('comment_karma', comment_karma) or ''
        )
        self.update_karma_view()

    def update_karma_view(self):
        if self.config['karma_view'] == 'icon':
            self.INDICATOR.set_label(self.karma, 'karma_label')
        else:
            self.builder.get_object('karma').set_label("Karma: %s" % self.karma)

    def toggle_karma_view(self, widget):
        """
        Show Karma next to the icon or in menu.
        Doesn't work on some DEs.
        """
        view = str(widget.get_name())

        if view != self.config['karma_view']:
            self.cfg_cls.set_key('karma_view', view)

        if view == 'icon':
            self.builder.get_object('karma').hide()
            self.update_karma_view()
        else:
            self.builder.get_object('karma').show()
            self.INDICATOR.set_label('', 'karma_label')
            self.update_karma_view()

    """
    Inbox handlers.
    """

    def set_inbox(self, count):
        self.builder.get_object('inbox').set_label("Inbox: %s" % count)
        desktop.update_counter(count)

    def open_inbox(self, widget):
        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.set_inbox(0)
        self.local_data['inbox_count'] = 0
        webbrowser.open('https://www.reddit.com/message/unread/', new=1, autoraise=True)

    def notifications_handler(self, widget):
        notifications = int(widget.get_name())
        if notifications != self.config.get('notifications'):
            self.cfg_cls.set_key('notifications', notifications)

    """
    Autostart
    """

    def autostart_handler(self, widget):
        active = widget.get_active()
        self.cfg_cls.set_key('autostart', active)
        autostart('add') if active else autostart('remove')

    def force_refresh_handler(self, widget):
        self.update_reddit_data()

    def about_handler(self, widget):
        self.builder.add_from_file(get_file('furikura/ui/about.xml'))
        about = self.builder.get_object('furi_kura_about')
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file(get_file('furikura/icons/furi-kura-logo.png')))
        about.connect("response", lambda d, r: d.destroy())
        about.show()

    """
    Menu handlers.
    """

    def build_menu(self):
        self.INDICATOR.set_menu(Gtk.Menu())
        reddit_data = self.request.get_user_info()
        signals = {
            'inbox_handler': self.open_inbox,
            'karma_handler': self.toggle_karma_view,
            'refresh_handler': self.set_refresh_interval,
            'notifications_handler': self.notifications_handler,
            'autostart_handler': self.autostart_handler,
            'subreddit_handler': self.subreddit_chooser.show_window,
            'force_refresh_handler': self.force_refresh_handler,
            'about': self.about_handler,
            'quit': self.quit
        }

        self.builder.add_from_file(get_file('furikura/ui/menu.xml'))
        self.builder.connect_signals(signals)

        menu = self.builder.get_object('furikura_menu')
        menu.show()

        self.update_appindicator(reddit_data)
        self.run_background(self.config.get('refresh_interval'))

        self.set_radio('refresh_interval')
        self.set_radio('karma_view')
        self.set_radio('notifications')
        self.set_checkbox('autostart')

        self.INDICATOR.set_menu(menu)

    def build_login_menu(self):

        def open_login(context):
            webbrowser.open(self.cfg_cls.LOGIN_URI, new=1, autoraise=True)

        login_menu = Gtk.Menu()
        item_login = Gtk.MenuItem('Login')
        item_separator = Gtk.SeparatorMenuItem()
        item_quit = Gtk.MenuItem('Quit')

        item_login.connect('activate', open_login)
        item_quit.connect('activate', self.quit)

        login_menu.append(item_login)
        login_menu.append(item_separator)
        login_menu.append(item_quit)
        login_menu.show_all()

        self.INDICATOR.set_menu(login_menu)

    def set_radio(self, item_id):
        view = self.builder.get_object(item_id).get_children()
        for child in view:
            if str(child.get_name()) == str(self.config.get(item_id)):
                child.set_active("True")

    def set_checkbox(self, item_id):
        checkbox = self.builder.get_object(item_id)
        checkbox.set_active(self.config.get(item_id, False))

    def mail_notify(self, inbox_count):
        """
        If inbox_count is unchanged from last update - exit the function.
        If new inbox_count is smaller - user read the message
        somewhere else (browser, phone app, etc).
        """
        notification_config = self.config.get('notifications')
        local_inbox_count = self.local_data.get('inbox_count', 0)

        if inbox_count == local_inbox_count:
            return
        elif inbox_count < local_inbox_count:
            self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            return

        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ATTENTION)

        if not notification_config:
            return

        if not self.services['notification']:
            self.services['notification'] = Notify.init(self.APPINDICATOR_ID)

        if notification_config == 1:
            message_data = self.request.get_last_message()
            header = "reddit mail from <b>{author}</b>".format(author=message_data['author'])
            body = message_data['body']
        else:
            header = "You have a new reddit mail"
            body = ''

        Notify.Notification.new(
            header,
            body,
            self.ICONS['main']
        ).show()

    """
    Subreddit
    """

    def subreddit_updates(self):
        self.subreddit_chooser.update_indicator()

    @staticmethod
    def main_loop():
        Gtk.main()

    def quit(self, widget):
        if self.services['timeout']:
            GObject.source_remove(self.services['timeout'])
        os.unlink(self.cfg_cls.LOCKFILE)
        Gtk.main_quit()
