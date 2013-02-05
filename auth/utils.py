# This is where we create methods that relate to this module
# but have no dependencies and are static.

from auth import models as auth_models

def authenticate(email, password):
    user = auth_models.User.all().filter('email =', email).fetch(1)

    if len(user):
        user = user[0]
        return password == user.password

    return False


