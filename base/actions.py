from base import models as base_models
from google.appengine.api import memcache
from google.appengine.ext import db

def notify_user(user, title, description, link):
    # Build notification
    notification = base_models.Notification(title=title,
                                            description=description,
                                            link=link)
    notification.put()

    # Attach to user
    user.notifications.append(notification.key())
    user.put()


def get_notification_by_key(key):
    notification = memcache.get(str(key))
    if notification:
        return notification

    notification = db.get(key)
    if notification:
        memcache.set(str(key), notification)
    return notification


def get_unread_notifications(user):

    notifications = [get_notification_by_key(note_key) for note_key in user.notifications]
    notifications = sorted(notifications,
                       key=lambda notification: notification.sent,
                       reverse=True)

    return notifications

