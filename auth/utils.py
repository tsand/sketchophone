import hashlib, uuid


def get_salt():
    return uuid.uuid4().hex


def salt_password(password, salt=None):
    if not salt:
        salt = get_salt()

    return hashlib.sha512(password + salt).hexdigest(), salt


