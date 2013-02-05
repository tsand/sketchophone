import os
from flask import Flask

app = Flask(__name__)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'this-is-just-our-dev-key-oh-so-secret'

from auth import urls as auth_urls
from base import urls as base_urls
from sketch import urls as sketch_urls

auth_urls.apply_urls(app)
base_urls.apply_urls(app)
sketch_urls.apply_urls(app)



if __name__ == '__main__':
    app.run(debug=True)