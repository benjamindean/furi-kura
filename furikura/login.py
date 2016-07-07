import time
from urllib.parse import urlencode

import requests
import requests.auth
from flask import Flask, abort, request

from .config import Config
from .utils import get_file

cfg_cls = Config()
app = Flask(__name__)


@app.route('/')
def homepage():
    try:
        with open(get_file('furikura/ui/login/login.html')) as html:
            login_html = html.read()
    except IOError:
        login_html = '<a href="%s">Authenticate with reddit</a>'

    return login_html % make_authorization_url()

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

    cfg_cls.set_key('access_token', tokens['access_token'])
    cfg_cls.set_key('refresh_token', tokens['refresh_token'])
    cfg_cls.set_key('token_expires', time.time() + 3600)

    try:
        with open(get_file('furikura/ui/login/success.html')) as html:
            success_html = html.read()
    except IOError:
        success_html = 'You have successfully logged in'

    time.sleep(3)

    from .indicator import FuriKuraIndicator
    ind = FuriKuraIndicator(cfg_cls)
    ind.build_menu()

    shutdown_server()
    return success_html

def make_authorization_url():
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {'client_id': cfg_cls.CLIENT_ID,
              'response_type': 'code',
              'state': state,
              'redirect_uri': cfg_cls.REDIRECT_URI,
              'duration': 'permanent',
              'scope': 'identity,privatemessages,read'}
    url = 'https://www.reddit.com/api/v1/authorize?' + urlencode(params)
    return url

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(cfg_cls.CLIENT_ID, "")
    post_data = {'grant_type': 'authorization_code',
                 'code': code,
                 'redirect_uri': cfg_cls.REDIRECT_URI}
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=client_auth,
        data=post_data,
        headers={'User-Agent': cfg_cls.USER_AGENT}
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
