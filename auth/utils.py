# This is where we create methods that relate to this module
# but have no dependencies and are static.

from auth import models as auth_models
import hashlib, uuid

def get_salt():
    return uuid.uuid4().hex

def salt_password(password, salt=None):
    if not salt:
        salt = get_salt()

    return hashlib.sha512(password + salt).hexdigest(), salt


def authenticate(email, password):
    user = auth_models.User.all().filter('email =', email).fetch(1)

    if len(user):
        user = user[0]
        salted_password, salt = salt_password(password, user.salt)
        return salted_password == user.password

    return False

