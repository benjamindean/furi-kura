import gi
import webbrowser

from .api import API
from .utils import get_file
from .utils import debug

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify
from gi.repository import GObject


class FuriKuraIndicator(object):
    # Init appindicator
    APPINDICATOR_ID = 'furikura_indicator'
    ICONS = {
        'active': get_file('furikura/icons/furi-active.png'),
        'attention': get_file('furikura/icons/furi-attention.png')
    }
    INDICATOR = AppIndicator3.Indicator.new(
        APPINDICATOR_ID,
        ICONS['active'],
        AppIndicator3.IndicatorCategory.COMMUNICATIONS
    )

    def __init__(self, config_storage):

        # Throwing config class here
        self.config_storage = config_storage

        # Instantiating API handler
        self.request = API(self.config_storage)

        # Getting initial config
        self.config = self.config_storage.config

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

        self.init_appindicator()

    def init_appindicator(self):
        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.INDICATOR.set_attention_icon(self.ICONS['attention'])

    def update_reddit_data(self):
        self.update_appindicator(self.request.get_user_info())
        return True

    """
    Background processing.
    """

    def update_appindicator(self, reddit_data):
        if not reddit_data: return
        self.set_inbox(reddit_data['inbox_count'])
        self.mail_notify(reddit_data['inbox_count'])
        self.set_karma(reddit_data['link_karma'], reddit_data['comment_karma'])
        self.local_data = reddit_data

    def run_background(self, interval):
        timeout = 10000 #interval * 60 * 1000
        self.services['timeout'] = GObject.timeout_add(timeout, self.update_reddit_data)

    def set_refresh_interval(self, widget):
        interval = int(widget.get_name())
        if interval != self.config.get('refresh_interval'):
            GObject.source_remove(self.services['timeout'])
            self.run_background(interval)
            self.config_storage.set_key('refresh_interval', interval)

    """
    Karma handlers.
    """

    def __compare_karma(self, karma_view, karma):
        if not self.local_data[karma_view]: return
        if self.local_data[karma_view] > karma:
            return '\u2193'
        elif self.local_data[karma_view] < karma:
            return '\u2191'

    def set_karma(self, link_karma, comment_karma):
        self.karma = "{link_arrow}{link} | {comment_arrow}{post}".format(
            link=link_karma,
            post=comment_karma,
            link_arrow=self.__compare_karma('link_karma', link_karma) or '',
            comment_arrow=self.__compare_karma('comment_karma', comment_karma) or ''
        )
        self.update_karma_view()

    def update_karma_view(self):
        view = self.config['karma_view']
        if view == 'icon': self.INDICATOR.set_label(self.karma, 'karma_label')
        else: self.builder.get_object('karma').set_label("Karma: %s" % self.karma)

    def toggle_karma_view(self, widget):
        view = str(widget.get_name())

        if view != self.config['karma_view']:
            self.config_storage.set_key('karma_view', view)

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

    def open_inbox(self, widget):
        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.set_inbox(0)
        self.local_data['inbox_count'] = 0
        webbrowser.open('https://www.reddit.com/message/unread/', new=1, autoraise=True)

    def notifications_handler(self, widget):
        notifications = int(widget.get_name())
        if notifications != self.config.get('notifications'):
            self.config_storage.set_key('notifications', notifications)

    """
    Menu handlers.
    """

    def build_menu(self):
        reddit_data = self.request.get_user_info()
        signals = {
            'inbox_handler': self.open_inbox,
            'karma_handler': self.toggle_karma_view,
            'refresh_handler': self.set_refresh_interval,
            'notifications_handler': self.notifications_handler,
            'quit': self.quit
        }

        self.builder.add_from_file(get_file('furikura/ui/menu.xml'))
        self.builder.connect_signals(signals)

        menu = self.builder.get_object('furikura_menu')
        menu.show_all()

        self.update_appindicator(reddit_data)
        self.run_background(self.config.get('refresh_interval'))

        self.set_radio('refresh_interval')
        self.set_radio('karma_view')
        self.set_radio('notifications')

        self.INDICATOR.set_menu(menu)

    def build_login_menu(self):

        def open_login(context):
            webbrowser.open(self.config_storage.LOGIN_URI, new=1, autoraise=True)

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

    def mail_notify(self, inbox_count):
        """
        If inbox_count is unchanged from last update - exit the function.
        If new inbox_count is smaller - user read the message
        somewhere else (browser, phone app, etc).
        """
        local_inbox_count = self.local_data.get('inbox_count')
        if inbox_count == local_inbox_count: return
        elif inbox_count < local_inbox_count:
            self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            return

        self.INDICATOR.set_status(AppIndicator3.IndicatorStatus.ATTENTION)

        if not self.config.get('notifications'): return

        if not self.services['notification']:
            self.services['notification'] = Notify.init(self.APPINDICATOR_ID)

        if self.config.get('notifications') == 1:
            message_data = self.request.get_last_message()
            header = "reddit mail from <b>{author}</b>".format(author=message_data['author'])
            body = message_data['body']
        else:
            header = "You have a new reddit mail"
            body = ''

        Notify.Notification.new(
            header,
            body,
            self.ICONS['active']
        ).show()

    def main_loop(self):
        Gtk.main()

    def quit(self, widget):
        if self.services['timeout']:
            GObject.source_remove(self.services['timeout'])
        Gtk.main_quit()
