# This is where we handle calls to the data store.
# These methods are usually called from the view
# For example
from auth import models as auth_models

def create_user(name):
    new_user = auth_models.User(username = name)
    new_user.put() #calling put on an data store object stores it in the data store

def find_user_by_username(name):
    user = auth_models.User.all().filter('username =', name).get()
    return user

def get_user_by_id(id):
    user = auth_models.User.all().filter('id=', id).get()
    return user

def check_username_exists(username):
    user = auth_models.User.all().filter('username =', username).fetch(1)

    if len(user):
        return True

    return False