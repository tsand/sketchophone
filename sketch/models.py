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



class Round(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)

    user = db.ReferenceProperty(User)

    SKETCH = 'sketch'
    TEXT = 'text'
    round_type = db.StringProperty(choices=[SKETCH, TEXT])

    data = db.BlobProperty(default=None)
