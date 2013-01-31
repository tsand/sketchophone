# This is where we generate the html data and or json
from flask.views import MethodView
from flask.templating import render_template
from flask import request

class UserView(MethodView):
    # get is called when we want to get html data or json when the url
    # that is assigned to it is called
    def get(self):
        context = {}

        # request args gets the url arguments
        # for example if we go to the url http://localhost:8001/user/?name=Jack
        # we can get the data stored after the question mark
        # so if we want the variable stored in name we can use this method

        # if the argument doesn't exist, for example the url http://localhost:8001/user/
        # we use the default value 'John' that is explicitly defined here
        context['name'] = request.args.get('name', 'John')

        # now we can pass the name we found from our url and pass it to our render
        # tool that replaces the {{name}} in user.html with the name we want!
        return render_template('user.html',  **context)