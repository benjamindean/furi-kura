from unittest import TestCase

from furikura.api import API
from furikura.config import Config
from furikura.indicator import FuriKuraIndicator

config_cls = Config()
indicator_cls = FuriKuraIndicator(config_cls)
api_cls = API(config_cls)


class TestFuriKuraIndicator(TestCase):
    def test_init_appindicator(self):
        self.assertIsNone(indicator_cls.init_appindicator())

    def test_update_reddit_data(self):
        self.assertTrue(indicator_cls.update_reddit_data())

    def test_update_appindicator(self):
        self.assertIsNone(indicator_cls.update_appindicator(api_cls.get_user_info()))

    # def test_run_background(self):
    #     self.fail()
    #
    # def test_set_refresh_interval(self):
    #     self.fail()
    #
    # def test_set_karma(self):
    #     self.fail()
    #
    # def test_update_karma_view(self):
    #     self.fail()
    #
    # def test_toggle_karma_view(self):
    #     self.fail()
    #
    # def test_set_inbox(self):
    #     self.fail()
    #
    # def test_open_inbox(self):
    #     self.fail()
    #
    # def test_notifications_handler(self):
    #     self.fail()
    #
    # def test_autostart_handler(self):
    #     self.fail()
    #
    # def test_force_refresh_handler(self):
    #     self.fail()
    #
    # def test_about_handler(self):
    #     self.fail()
    #
    # def test_build_menu(self):
    #     self.fail()
    #
    # def test_build_login_menu(self):
    #     self.fail()
    #
    # def test_set_radio(self):
    #     self.fail()
    #
    # def test_set_checkbox(self):
    #     self.fail()
    #
    # def test_mail_notify(self):
    #     self.fail()
    #
    # def test_subreddit_updates(self):
    #     self.fail()
    #
    # def test_main_loop(self):
    #     self.fail()
    #
    # def test_quit(self):
    #     self.fail()
