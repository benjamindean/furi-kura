import os
from unittest import TestCase

import requests

from furikura import utils


def test_request():
    requests.get('https://example.com')

class TestUtils(TestCase):
    def test_get_file(self):
        self.assertEqual(utils.get_file("testfile"), "/usr/share/testfile")

    def test_check_connection(self):
        self.addTypeEqualityFunc(type, utils.check_connection(test_request))

    def test_autostart(self):
        utils.autostart('add')
        self.assertTrue(os.path.islink(os.path.expanduser('~/.config/autostart/furikura.desktop')))

        utils.autostart('remove')
        self.assertFalse(os.path.islink(os.path.expanduser('~/.config/autostart/furikura.desktop')))

