from unittest import TestCase
from furikura import utils

class TestUtils(TestCase):
    def test_get_file(self):
        self.assertEqual(utils.get_file("testfile"), "/usr/share/testfile")
