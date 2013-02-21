import json

from flask import abort
from flask.views import MethodView, View
from flask.templating import render_template

from base import cron

class HomeView(MethodView):
    def get(self):
        return render_template('home.html')


class AboutView(View):
	def dispatch_request(self):
		return render_template('about.html' )


class Cron(View):
    def dispatch_request(self, function):
        try:
            function_call = getattr(cron, function)
            function_call()
            return json.dumps('Cron Job Running: %s' % function)
        except AttributeError:
            abort(404)