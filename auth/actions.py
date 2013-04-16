# This is where we handle calls to the data store.
# These methods are usually called from the view

from auth import models as auth_models
from auth import utils as auth_utils
from google.appengine.ext import db


# User Retrieval
def get_user_by_key(key):
    return db.get(key)

def get_user_by_flask_user(user):
    if not user.is_anonymous():
        return get_user_by_key(user.key())
    return None

def get_user_by_email(email):
    user = auth_models.User.all().filter('email =', email).get()
    return user


def get_user_by_id(id):
    user = auth_models.User.all().filter('id =', id).get()
    return user


def get_user_by_facebook_id(facebook_id):
    user = auth_models.User.all().filter('facebook_id =', facebook_id).get()
    return user


def get_user_by_registration_id(id):
    user = auth_models.User.all().filter('registration_id =', id).get()
    return user


def guess_users_by_username(name):
    users = auth_models.User.all().filter('username >=', name).filter('username <', name + u'\ufffd')
    return users


def delete_user(username):
    new_user = auth_models.User(username=username)
    new_user.delete()


# User Attribute Verification
def check_username(username):
    user = auth_models.User.all().filter('registered = ', True).filter('username =', username).fetch(1)
    if user:
        return True
    return False


def check_email(email):
    user = auth_models.User.all().filter('registered = ', True).filter('email =', email).fetch(1)
    if user:
        return True
    return False


# User Authentication
def authenticate(email, password):
    user = auth_models.User.all().filter('email =', email).fetch(1)

    if user:
        user = user[0]
        salted_password, salt = auth_utils.salt_password(password, user.salt)
        return salted_password == user.password

    return False
