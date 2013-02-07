# This is where we handle calls to the data store.
# These methods are usually called from the view

from auth import models as auth_models
from auth import utils as auth_utils

def create_user(username):
    new_user = auth_models.User(username = username)
    new_user.put() # calling 'put' on an data store object stores it in the data store

def get_user_by_username(name):
    user = auth_models.User.all().filter('username =', name).get()
    return user

def get_user_by_id(id):
    user = auth_models.User.all().filter('id =', id).get()
    return user

def get_user_by_facebook_id(facebook_id):
    user = auth_models.User.all().filter('facebook_id =', facebook_id).get()
    return user

def check_username(username):
    user = auth_models.User.all().filter('username =', username).fetch(1)
    if len(user):
        return True
    return False

def check_email(email):
    user = auth_models.User.all().filter('email =', email).fetch(1)
    if len(user):
        return True
    return False

def authenticate(username, password):
    user = auth_models.User.all().filter('username =', username).fetch(1)

    if len(user):
        user = user[0]
        salted_password, salt = auth_utils.salt_password(password, user.salt)
        return salted_password == user.password

    return False