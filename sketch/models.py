from google.appengine.ext import db
from auth import models as auth_models


class Game(db.Model):
	title = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	PUBLIC = 'public'
	PRIVATE = 'private'
	PERMISSION_CHOICES = [PUBLIC,PRIVATE]
	perms = db.StringProperty(choices=PERMISSION_CHOICES)
	number_of_rounds = db.IntegerProperty()
	guests = db.ListProperty(db.Key) 


class Round(db.Model):
	created = db.DateTimeProperty(auto_now_add=True)
	SKETCH = 'sketch'
	TEXT = 'text'
	ROUND_TYPES = [SKETCH,TEXT]
	round_type = db.StringProperty(choices=ROUND_TYPES)
	data = db.BlobProperty(default=None)
	user = db.ReferenceProperty(auth_models.User)