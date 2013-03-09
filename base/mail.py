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

def send_created_game_email(recipient, game_title, game_link, created_by):
    message = BaseEmail()
    message.subject = "New Sketchophone Game: %s" % game_title
    message.to = recipient

    message.body = render_template('email/registration.txt',
                                   game_title=game_title,
                                   game_link=game_link,
                                   created_by=created_by)
    message.html = render_template('email/registration.html',
                                   game_title=game_title,
                                   game_link=game_link,
                                   created_by=created_by)

    message.send_deferred()


