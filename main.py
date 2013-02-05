import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

from google.appengine.ext.webapp.util import run_wsgi_app

from flask import Flask

import auth
from auth import urls as auth_urls
from base import urls as base_urls
from sketch import urls as sketch_urls

app = Flask(__name__)
app.secret_key = 'i-hope-no-one-can-guess-our-secret-dev-key'

# Apply Urls
auth_urls.apply_urls(app)
base_urls.apply_urls(app)
sketch_urls.apply_urls(app)

auth.initialize(app)


if __name__ == '__main__':
    run_wsgi_app(app)