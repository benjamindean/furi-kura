import time
import requests.auth

from .utils import check_connection


class API(object):
    def __init__(self, config_storage):
        self.config_storage = config_storage
        self.config = self.config_storage.config
        self.refresh_token = self.config.get('refresh_token')
        self.token_expires = self.config.get("token_expires")
        self.headers = self.config_storage.get_headers(self.config.get('access_token'))

    @check_connection
    def get_new_token(self):
        """
        Get new token using refresh token.
        """
        client_auth = requests.auth.HTTPBasicAuth(self.config_storage.CLIENT_ID, "")
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token',
            auth=client_auth,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            },
            headers={
                "User-Agent": self.config_storage.USER_AGENT
            }
        )

        access_token = response.json()['access_token']
        self.token_expires = time.time() + 3600
        self.config_storage.set_key('token_expires', self.token_expires)
        self.config_storage.set_key('access_token', access_token)
        self.set_token(access_token)
        print("Token refreshed with %s, until %s" % (response.json()['access_token'], time.time() + 3600))

    def check_token(self):
        """
        Check if current token expired
        and get new one if it is.
        """
        if time.time() >= self.token_expires:
            self.get_new_token()

    def set_token(self, token):
        """
        Set token config value and update headers.
        """
        self.config_storage.set_key('access_token', token)
        self.headers = self.config_storage.get_headers(token)

    @check_connection
    def get_user_info(self):
        """
        Get current user info.
        """
        self.check_token()
        response = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
        return response.json()

    @check_connection
    def get_subreddit(self, subreddit, posts_type, posts_limit='5'):
        """
        Get subreddit info.
        """
        self.check_token()
        posts_list = []

        response = requests.get(
            'https://oauth.reddit.com/r/%s/%s' % (subreddit, posts_type),
            headers=self.headers,
            params={'limit': posts_limit}
        )
        posts = response.json()['data']['children']

        for post in posts:
            posts_list.append({
                'link': post['data']['url'],
                'title': post['data']['title'],
                'upvotes': post['data']['ups']
            })

        return posts_list

    @check_connection
    def get_last_message(self):
        """
        Get contents of the last unread message.
        Should run only if notifications setting is 1.
        """
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
