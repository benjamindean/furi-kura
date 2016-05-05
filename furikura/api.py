import time
import requests.auth


class API(object):
    def __init__(self, config_storage):
        print("Init API")
        self.config_storage = config_storage
        self.config = self.config_storage.config

        self.refresh_token = self.config.get('refresh_token')
        self.token_expires = self.config.get("token_expires")
        self.headers = self.config_storage.set_headers(self.config.get('access_token'))

    def get_new_token(self):
        client_auth = requests.auth.HTTPBasicAuth(self.config_storage.CLIENT_ID, "")
        post_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=client_auth,
            data=post_data,
            headers={"User-Agent": self.config_storage.USER_AGENT}
        )

        access_token = response.json()['access_token']
        self.token_expires = time.time() + 3600
        self.config_storage.set_key('token_expires', self.token_expires)
        self.config_storage.set_key('access_token', access_token)
        self.set_token(access_token)
        print("Token refreshed with %s, until %s" % (response.json()['access_token'], time.time() + 3600))

    def check_token(self):
        return time.time() >= self.token_expires

    def set_token(self, token):
        self.config_storage.set_key('access_token', token)
        self.headers = self.config_storage.set_headers(token)

    def fetch_user_info(self):
        if self.check_token():
            self.get_new_token()
        response = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
        return response.json()

    def get_last_message(self):
        response = requests.get(
            'https://oauth.reddit.com/message/unread',
            headers=self.headers,
            params={'limit': 1}
        )
        post_data = response.json()['data']['children'][0]['data']

        return {
            'body': post_data['body'],
            'author': post_data['author']
        }
