from google.appengine.ext import db
from datetime import datetime
from google.appengine.api import memcache
from auth.models import User


class Game(db.Model):
    title = db.StringProperty()

    def put(self):
        db.put(self)
        memcache.set(str(self.key()), self)


    created = db.DateTimeProperty(auto_now_add=True)
    created_by = db.ReferenceProperty(User)

    PUBLIC = 'public'
    PRIVATE = 'private'
    perms = db.StringProperty(choices=[PUBLIC, PRIVATE])

    max_rounds = db.IntegerProperty()
    num_rounds = db.IntegerProperty()
    def is_over(self):
        return self.num_rounds >= self.max_rounds

    occupant_name = db.StringProperty()
    date_occupied = db.DateTimeProperty()
    occupied_session = db.TextProperty()

    def occupy(self, user, session):
        self.occupant_name = user.display_name
        self.occupied_session = session
        self.date_occupied = datetime.now()
        
    def is_occupied(self):
        return bool(self.occupied_session)

    def session_is_occupant(self, session):
        if session:
            return self.occupied_session == session
        return False

    def evict_occupancy(self):
        if self.is_occupied():
            self.occupant_name = None
            self.date_occupied = None
            self.occupied_session = None
            self.put()

    locked_length = 2
    locked_users = db.TextProperty(default=':'.join([''for x in xrange(locked_length)]))

    def is_locked_out(self, user, session):
        convicts = self.get_locked_users()
        if user.is_anonymous():
            return session in convicts
        else:
            return str(user.key()) in convicts

    def get_locked_users(self):
        return self.locked_users.split(':')

    def set_locked_users(self, user_list):
        self.locked_users = ':'.join(user_list)

    def updated_locked_users(self, user, session):
        identifier = ''
        if not user or user.is_anonymous():
            identifier = session
        else:
            identifier = str(user.key()) 
        inmate_list = self.get_locked_users()
        freed_user = inmate_list.pop(0)
        inmate_list.append(identifier)
        self.set_locked_users(inmate_list)
        return freed_user


class Round(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)

    def get_date_formatted(self):
        if self.created:
            return self.created.strftime("%m/%d/%y %I:%M %p")
        return ''

    def put(self):
        db.put(self)
        memcache.set(str(self.key()), self)

    user = db.ReferenceProperty(User)

    is_banned = db.BooleanProperty(default=False)
    is_flagged = db.BooleanProperty(default=False)

    SKETCH = 'sketch'
    STORY = 'story'
    round_type = db.StringProperty(choices=[SKETCH, STORY])

    data = db.TextProperty()

    def get_data(self):
        import json
        if self.round_type == self.SKETCH:
            return json.loads(self.data)
        return self.data

