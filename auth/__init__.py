from auth import models as auth_models

from resources.flask_login import LoginManager

from models import User, Anonymous

login_manager = LoginManager()

def initialize(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(id):
    return auth_models.User.get_by_id(int(id))