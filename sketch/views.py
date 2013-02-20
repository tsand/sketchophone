from flask.views import MethodView
from flask.templating import render_template
from flask import request
import json
from google.appengine.ext import db
from sketch import actions as sketch_actions

import logging

class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')

class CreationWizard(MethodView):
	def get(self):
		return render_template('/create_game/wizard.html')
	def post(self):
		json_data = json.loads(request.data)
		j_form = json_data.get('form',None)

		if j_form is not None:
			friend_keys = [db.Key(friend_key) for friend_key in j_form.get('friends',[])]
			first_round_text = str(j_form.get('start_text',''))
			num_of_rounds = int(j_form.get('num_of_rounds',2))
			perms = j_form.get('perms','public')
			title = j_form.get('name', 'foo')

			game = sketch_actions.create_game(first_round_text, 
												title, 
												perms, 
												friend_keys, 
												num_of_rounds)


			return json.dumps({'success':True})

		return json.dumps({'success':False})
		



