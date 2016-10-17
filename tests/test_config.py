import os
from unittest import TestCase

from furikura import config

config_cls = config.Config()


class TestConfig(TestCase):
    def test_get_headers(self):
        token = "test_token"
        self.assertEqual(
            config_cls.get_headers(token),
            {"Authorization": "bearer %s" % token, "User-Agent": config_cls.USER_AGENT}
        )

    def test_read_config(self):
        self.addTypeEqualityFunc(dict, config_cls.read_config())

    def test_write_config(self):
        config_cls.write_config()
        self.assertEqual(os.path.isfile(config_cls.CONFIG_FILE), True)

    def test_set_key(self):
        config_cls.set_key('testing_key', 'testing_value')
        self.assertIsNone(config_cls.set_key('testing_key', 'testing_value'))
        self.assertEqual(config_cls.get_value('testing_key'), 'testing_value')

    def test_get_value(self):
        config_cls.set_key('testing_key', 'testing_value')
        self.assertEqual(config_cls.get_value('testing_key'), 'testing_value')
