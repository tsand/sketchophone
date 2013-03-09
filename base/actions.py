from base import models as base_models

def notify_user(user, title, description, link):
    # Build notification
    notification = base_models.Notification(title=title,
                                            description=description,
                                            link=link)
    notification.put()

    # Attach to user
    user.notifications.append(notification.key())
    user.put()