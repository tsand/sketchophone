# This is where we handle calls to the data store.
# These methods are usually called from the view

from auth import models as auth_models
from auth import utils as auth_utils
from datetime import datetime, timedelta
from google.appengine.ext import db


# User Retrieval
def get_user_by_key(key):
    return db.get(key)


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


# Batch User Retrieval
def delete_expired_users():
    users = auth_models.User.all().filter('registered =', False).run()
    expiry_time = datetime.now() - timedelta(1)
    for user in users:
        if user.created < expiry_time:
            user.delete()


# Testing
def create_registered_user(username, password):
    """
    Only use for testing!
    """
    password, salt = auth_utils.salt_password(password)
    user = auth_models.User(
        username=username,
        password=password,
        salt=salt,
        email='%s@test.com' % username,
        registered=True
    )
    user.put()
    return user


def generate_random_users(num=25):
    """
    You can run this from the interactive console on your local host
    http://localhost:8001/_ah/admin/interactive
    -----
    from auth import actions
    actions.generate_random_users()
    """
    import random
    for n in xrange(num):
        rand_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for abc in range(7))
        create_registered_user(rand_string, rand_string)
