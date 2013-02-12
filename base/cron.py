from google.appengine.ext import deferred

from auth import actions as auth_actions


def clean_users():
    deferred.defer(auth_actions.delete_expired_users)
