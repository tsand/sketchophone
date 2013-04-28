from google.appengine.ext import db
from resources.flask_login import AnonymousUser


class User(db.Model):
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
    games = db.ListProperty(db.Key)
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

    # Games
    def attach_game(self, game_key):
        if game_key not in self.games:
            self.games.append(game_key)
            self.put()

    def get_games(self):
        return [game for game in db.get(self.games) if game is not None]

    def get_game_count(self):
        return len(self.games)

    # Notification
    def get_notifications(self):
        notifications = [db.get(note) for note in self.notifications]
        notifications = sorted(notifications,
                               key=lambda notification: notification.sent,
                               reverse=True)
        return notifications

    @property
    def notification_count(self):
        return len(self.notifications)

    @property
    def unread_notification_count(self):
        count = 0
        for notification in self.get_notifications():
            if not notification.read:
                count += 1
        return count

    def read_notifications(self):
        for notification in self.get_notifications():
            notification.read = True
            notification.put()


class Anonymous(AnonymousUser):
    username = "Anonymous"

    @property
    def display_name(self):
        return self.username

    @property
    def administrator(self):
        return False

    def attach_game(self, game_key):
        return False

    def key(self):
        return ''