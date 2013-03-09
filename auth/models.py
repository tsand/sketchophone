# This is where we create data models to be stored in the data store.
# These are usually called from actions
from base.models import Notification
from google.appengine.ext import db
from resources.flask_login import AnonymousUser


class User(db.Model):
    # https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses

    username = db.StringProperty()
    password = db.StringProperty()
    salt = db.StringProperty()
    email = db.EmailProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    administrator = db.BooleanProperty(default=False)

    # Facebook
    name = db.StringProperty()
    facebook_id = db.StringProperty()

    # Registration Details
    registration_id = db.StringProperty()
    registered = db.BooleanProperty(default=False)

    # Game Stuff
    notifications = db.ListProperty(db.Key)
    invites = db.StringListProperty()



    @property
    def display_name(self):
        if self.name:
            return self.name

        elif self.username:
            return self.username

        else:
            return self.email

    def get_id(self):
        return self.key().id()

    def is_registered(self):
        return self.registered

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    # User type
    def is_facebook_user(self, only=False):
        if only:
            return bool(self.facebook_id) and not self.is_base_user()
        return bool(self.facebook_id)

    def is_base_user(self, only=False):
        if only:
            return bool(self.username) and not self.is_facebook_user()
        return bool(self.username)

    # Notification Handling
    @property
    def notification_count(self):
        return len(self.notifications)

    def notify(self, notification):
        self.notifications = self.notifications + notification.key()
        self.put()

    def read_notifications(self):
        self.notifications = 0


class Anonymous(AnonymousUser):
    username = "Anonymous"

    @property
    def display_name(self):
        return self.username

