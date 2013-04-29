from auth.models import User, Anonymous
from flask import session
from resources.flask_login import LoginManager
from resources.flask_oauth import OAuth
from auth import actions
import settings

login_manager = LoginManager()

facebook = OAuth().remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=settings.FACEBOOK_APP_ID,
    consumer_secret=settings.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

def initialize(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(id):
    return actions.get_user_by_id(int(id))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token'), settings.FACEBOOK_APP_SECRET