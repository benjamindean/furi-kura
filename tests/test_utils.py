import os
from unittest import TestCase

import requests

from furikura import utils
from furikura.config import Config

config_cls = Config()

def test_request():
    requests.get('http://example.com')

class TestUtils(TestCase):
    def test_get_file(self):
        self.assertEqual(utils.get_file("testfile"), "/usr/share/testfile")

    @utils.check_connection
    def test_check_connection(self):
        valid = requests.get('http://example.com')
        invalid = requests.get('fake_domain')
        self.assertTrue(valid.ok)
        self.assertFalse(invalid.ok)

    def test_autostart(self):
        os.makedirs(os.path.expanduser('~/.config/autostart/'), exist_ok=True)

        utils.autostart('add')
        self.assertTrue(os.path.islink(os.path.expanduser('~/.config/autostart/furikura.desktop')))

        utils.autostart('remove')
        self.assertFalse(os.path.islink(os.path.expanduser('~/.config/autostart/furikura.desktop')))

    def test_check_lock(self):
        os.makedirs(os.path.expanduser('~/.config/furikura/'), exist_ok=True)

        utils.check_lock()
        self.assertTrue(os.path.isfile(config_cls.LOCKFILE))

    def test_debug(self):
        self.addTypeEqualityFunc(type, utils.debug(test_request))


