import time
import requests.auth


class API(object):
    def __init__(self, config_storage):
        self.config_storage = config_storage
        self.config = self.config_storage.config
        self.refresh_token = self.config.get('refresh_token')
        self.token_expires = self.config.get("token_expires")
        self.headers = self.config_storage.set_headers(self.config.get('access_token'))

    def get_new_token(self):
        """
        Get new token using refresh token.
        """
        try:
            client_auth = requests.auth.HTTPBasicAuth(self.config_storage.CLIENT_ID, "")
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False

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
        Check if current token expired.
        """
        return time.time() >= self.token_expires

    def set_token(self, token):
        """
        Set token config value and update headers.
        """
        self.config_storage.set_key('access_token', token)
        self.headers = self.config_storage.set_headers(token)

    def get_user_info(self):
        """
        Get current user info.
        """
        if self.check_token():
            self.get_new_token()

        try:
            response = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.headers)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False

        return response.json()

    def get_last_message(self):
        """
        Get contents of the last unread message.
        Should run only if notifications setting is 1.
        """
        try:
            response = requests.get(
                'https://oauth.reddit.com/message/unread',
                headers=self.headers,
                params={'limit': 1}
            )
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False

        post_data = response.json()['data']['children'][0]['data']

        return {
            'body': post_data['body'],
            'author': post_data['author']
        }
