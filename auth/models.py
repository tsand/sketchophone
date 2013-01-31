# This is where we create data models to be stored in the data store.
# These are usually called from actions
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty()
    # a list of data different store properties can be found here
    # https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses