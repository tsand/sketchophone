# This is where we handle calls to the data store.
# These methods are usually called from the view

from auth import models as auth_models

def create_user(username):
    new_user = auth_models.User(username = username)
    new_user.put() # calling 'put' on an data store object stores it in the data store

def get_user_by_username(name):
    user = auth_models.User.all().filter('username =', name).get()
    return user

def get_user_by_id(id):
    user = auth_models.User.all().filter('id =', id).get()
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

def guess_users_by_username(name):
    users = auth_models.User.all().filter('username >=', name).filter('username <', name + u'\ufffd')
    return users