from google.appengine.ext import deferred

from tools import scripts
from sketch import actions as sketch_actions


def clean_users():
    deferred.defer(scripts.delete_expired_users())


def evict_lazy_people():
    deferred.defer(sketch_actions.evict_lazy_users)
