from flask.views import MethodView, View
from flask.templating import render_template

class HomeView(MethodView):
    def get(self):
        return render_template('home.html' )

class AboutView(View):
	def dispatch_request(self):
		return render_template('about.html' )