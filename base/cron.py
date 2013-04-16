from google.appengine.ext import deferred

from auth import actions as auth_actions
from sketch import actions as sketch_actions


def clean_users():
    deferred.defer(auth_actions.delete_expired_users)

def evict_lazy_people():
    deferred.defer(sketch_actions.evict_lazy_users)
