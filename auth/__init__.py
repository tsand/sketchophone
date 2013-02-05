from auth import models as auth_models
from lib.flask_login import LoginManager
from models import User

login_manager = LoginManager()

def initialize(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return auth_models.User.get_by_id(int(id))