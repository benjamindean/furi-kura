import json
import os.path


class Config(object):
    CONFIG_FILE = os.path.expanduser("~/.furikura")
    DUMP_FILE = os.path.expanduser("~/.furikura_dump")

    CLIENT_ID = "RQftQ0QKd9ZCDA"
    REDIRECT_URI = "http://localhost:65010/reddit_callback"
    USER_AGENT = "FuriKuraForReddit/0.1 by benjaminabel"

    def __init__(self):
        print("Init config")
        self.config = self.read_config()
        self.headers = {}

    def set_headers(self, token):
        print("Get headers")
        self.headers = {"Authorization": "bearer %s" % token, "User-Agent": self.USER_AGENT}
        return self.headers

    def read_config(self):
        print("Reading config")
        if not os.path.isfile(self.CONFIG_FILE):
            self.write_config()
        with open(self.CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)

    def write_config(self):
        print("Writing config")
        config_dict = {
            'refresh_interval': 1,
            'karma_view': 'menu'
        }
        with open(self.CONFIG_FILE, 'w') as config_file:
            json.dump(config_dict, config_file)

    def set_key(self, key, value):
        print("Set key: ", key)
        self.config[key] = value
        with open(self.CONFIG_FILE, 'w') as config_file:
            json.dump(self.config, config_file)

    def get_key(self, key):
        print("Get key: ", key)
        return self.config.get(key)
