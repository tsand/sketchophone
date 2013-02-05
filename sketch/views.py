from flask.views import MethodView
from flask.templating import render_template

class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')