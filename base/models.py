from google.appengine.ext import db
from google.appengine.api import memcache

class Notification(db.Model):

    title = db.StringProperty()
    description = db.StringProperty(multiline=True)
    link = db.StringProperty()
    sent = db.DateTimeProperty(auto_now_add=True)
    read = db.BooleanProperty(default=False)

    def put(self):
        db.put(self)
        memcache.set(str(self.key()), self)