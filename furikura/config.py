import json
import os.path


class Config(object):
    """
    Create, update and store applications config.
    """

    CONFIG_FILE = os.path.expanduser('~/.config/furikura/furikura')
    CLIENT_ID = 'RQftQ0QKd9ZCDA'
    LOGIN_ADDRESS = 'http://localhost:65010'
    REDIRECT_URI = LOGIN_ADDRESS + '/reddit_callback'
    USER_AGENT = 'FuriKuraForReddit/0.1 by benjaminabel'

    def __init__(self):
        print("Init config")
        self.config = self.read_config()
        self.headers = {}

    def set_headers(self, token):
        """
        Setting authorisation headers with USER_AGENT and Access Token and
        returning it.
        """
        print("Set headers")
        self.headers = {"Authorization": "bearer %s" % token, "User-Agent": self.USER_AGENT}
        return self.headers

    def read_config(self):
        """
        Return the contents of a config file.
        If file doesn't exist - create it first.
        """
        print("Reading config")
        if not os.path.isfile(self.CONFIG_FILE):
            self.write_config()
        with open(self.CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)

    def write_config(self):
        """
        Create config file with some default values.
        """
        print("Writing config")
        config_dict = {
            'refresh_interval': 1,
            'karma_view': 'menu',
            'notifications': 1
        }
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as config_file:
            json.dump(config_dict, config_file)

    def set_key(self, key, value):
        """
        Create or update config key.
        """
        if self.config.get(key) != value:
            print("Set key: ", key)
            self.config[key] = value
            with open(self.CONFIG_FILE, 'w') as config_file:
                json.dump(self.config, config_file)

    def get_value(self, key):
        """
        Get value of a config key.
        """
        print("Get key: ", key)
        return self.config.get(key)
