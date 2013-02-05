from flask.views import MethodView, View
from flask.templating import render_template

class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')
		
class AboutView(View):
	def get(self):
		return render_templage('about.html')