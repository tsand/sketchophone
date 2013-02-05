# This is where we create data models to be stored in the data store.
# These are usually called from actions
from google.appengine.ext import db
from lib.flask_login import AnonymousUser

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    salt = db.StringProperty()
    email = db.EmailProperty()
    created = db.DateTimeProperty(auto_now=True)
#    facebook_id = db.StringProperty()
#    https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses

    def get_id(self):
        return self.key().id()

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class Anonymous(AnonymousUser):
    username = "Anonymous"