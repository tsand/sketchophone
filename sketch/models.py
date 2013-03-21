from google.appengine.ext import db
from auth.models import User


class Game(db.Model):
    title = db.StringProperty()

    created = db.DateTimeProperty(auto_now_add=True)
    created_by = db.ReferenceProperty(User)

    PUBLIC = 'public'
    PRIVATE = 'private'
    perms = db.StringProperty(choices=[PUBLIC, PRIVATE])

    number_of_rounds = db.IntegerProperty()


    locked_length = 5
    locked_users = db.StringProperty(default=':'.join([''for x in xrange(locked_length)]))

    def get_locked_users(self):
        return self.locked_users.split(':')

    def set_locked_users(self, user_list):
        self.locked_users = ':'.join(user_list)

    def updated_locked_users(self, new_user_key):
        new_user_key = str(new_user_key) if new_user_key is not None else ''

        inmate_list = self.get_locked_users()
        freed_user = inmate_list.pop(0)
        inmate_list.append(new_user_key)
        self.set_locked_users(inmate_list)
        return freed_user


class Round(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)

    user = db.ReferenceProperty(User)

    SKETCH = 'sketch'
    STORY = 'story'
    round_type = db.StringProperty(choices=[SKETCH, STORY])

    data = db.TextProperty()

