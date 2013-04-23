from google.appengine.ext import db


class Notification(db.Model):

    title = db.StringProperty()
    description = db.StringProperty(multiline=True)
    link = db.StringProperty()
    sent = db.DateTimeProperty(auto_now_add=True)
    read = db.BooleanProperty(default=False)