import time
import requests
import requests.auth

from urllib.parse import urlencode
from flask import Flask, abort, request

from .config import Config
from . import utils

config_storage = Config()
app = Flask(__name__)


@app.route('/')
def homepage():
    try:
        with open(utils.get_file('furikura/ui/login/login.html')) as html:
            text = html.read()
    except IOError:
        text = '<a href="%s">Authenticate with reddit</a>'

    return text % make_authorization_url()


@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    tokens = get_token(code)

    config_storage.set_key('access_token', tokens['access_token'])
    config_storage.set_key('refresh_token', tokens['refresh_token'])
    config_storage.set_key('token_expires', time.time() + 3600)

    try:
        with open(utils.get_file('furikura/ui/login/success.html')) as html:
            text = html.read()
    except IOError:
        text = 'You have successfully logged in'

    from .indicator import FuriKuraIndicator
    ind = FuriKuraIndicator(config_storage)
    ind.build_menu()
    shutdown_server()

    return text


def make_authorization_url():
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {'client_id': config_storage.CLIENT_ID,
              'response_type': 'code',
              'state': state,
              'redirect_uri': config_storage.REDIRECT_URI,
              'duration': 'permanent',
              'scope': 'identity,privatemessages'}
    url = 'https://www.reddit.com/api/v1/authorize?' + urlencode(params)
    return url


def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(config_storage.CLIENT_ID, "")
    post_data = {'grant_type': 'authorization_code',
                 'code': code,
                 'redirect_uri': config_storage.REDIRECT_URI}
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=client_auth,
        data=post_data,
        headers={'User-Agent': config_storage.USER_AGENT}
    )
    return response.json()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def save_created_state(state):
    pass


def is_valid_state(state):
    return True


def run(*args):
    app.run(debug=False, port=65010)
