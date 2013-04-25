import json

from flask import abort, request
from flask.views import MethodView, View
from flask.templating import render_template

from base import cron


class HomeView(MethodView):
    def get(self):
        reset_app2home = bool(request.args.get('show_popup', ''))
        return render_template('home.html', reset_app2home=reset_app2home)


class AboutView(View):
    def dispatch_request(self):
        return render_template('about.html')


class InstructionsView(View):
    def dispatch_request(self):
        return render_template('instructions.html')


class AppsView(View):
    def dispatch_request(self):
        return render_template('app.html')


class Cron(View):
    def dispatch_request(self, function):
        try:
            function_call = getattr(cron, function)
            function_call()
            return json.dumps('Cron Job Running: %s' % function)
        except AttributeError:
            abort(404)