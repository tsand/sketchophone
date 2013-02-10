from google.appengine.api import mail
from google.appengine.ext import deferred

import settings

def send_email(recipient, subject, body):

    sender="Sketchophone <%s>" % settings.SUPPORT_EMAIL
    deferred.defer(mail.send_mail, sender=sender, to=recipient, subject=subject, body=body)