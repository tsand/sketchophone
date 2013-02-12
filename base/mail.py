from google.appengine.api import mail
from google.appengine.ext import deferred

from flask import render_template

import settings


class BaseEmail(mail.EmailMessage):

    sender = "Sketchophone <%s>" % settings.SUPPORT_EMAIL

    def send_deferred(self):
        deferred.defer(self.send)


def send_registration_email(recipient, registration_url):
    message = BaseEmail()
    message.subject = "Sketchophone Account Verification"
    message.to = recipient

    message.body = render_template('email/registration.txt', registration_url=registration_url)
    message.html = render_template('email/registration.html', registration_url=registration_url)

    message.send_deferred()


