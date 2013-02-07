from flask.views import MethodView
from flask.templating import render_template
from flask import request
import json



import logging

class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')

class CreationWizard(MethodView):
	def get(self):
		return render_template('/create_game/wizard.html')
	def post(self):
		friends = request.args.get('friends','')
		friend_list = friends.split(',')

		game_type = request.args.get('type','lin')
		privacy = request.args.get('privacy','public')

		# todo build out game model!

		logging.info("%s\n %s\n %s\n" % (friend_list, game_type, privacy))
		return json.dumps({})
		



