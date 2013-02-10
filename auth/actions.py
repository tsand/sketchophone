# This is where we handle calls to the data store.
# These methods are usually called from the view

from auth import models as auth_models
from auth import utils as auth_utils

from datetime import datetime, timedelta

# User Creation/Deletion
def create_user(username):
    new_user = auth_models.User(username = username)
    new_user.put() # calling 'put' on an data store object stores it in the data store

def delete_user(username):
    new_user = auth_models.User(username = username)
    new_user.delete()


# User Retrieval
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

# Batch User Retrieval
def delete_expired_users():
    users = auth_models.User.all().filter('registered =', False).run()
    expiry_time = datetime.now() - timedelta(1)
    for user in users:
        if user.created < expiry_time:
            user.delete()

