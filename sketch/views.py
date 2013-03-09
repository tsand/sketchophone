import json

from flask import abort, redirect, url_for, request
from flask.views import MethodView
from flask.templating import render_template
from google.appengine.ext import db
from resources.flask_login import current_user
from sketch import actions as sketch_actions


class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')

class CreationWizard(MethodView):
    def get(self):
        return render_template('/create_game/wizard.html',
                               current_user=current_user)

    def post(self):

        j_form = json.loads(request.data).get('form', None)

        guests = [db.get(key).key() for key in j_form.get('guests', None)]

        if j_form is not None:
            sketch_actions.create_game(
                first_round_text=str(j_form.get('start_text', '')),
                title=str(j_form.get('name', 'foo')),
                perms=str(j_form.get('perms', 'public')),
                guests=guests,
                num_of_rounds=int(j_form.get('num_of_rounds', 3))
            )

            return json.dumps({'success':True})

        return json.dumps({'success':False})



class SearchGamesView(MethodView):
    def get(self):
        public_games = sketch_actions.get_latest_public_games()
        private_games = sketch_actions.get_private_games(current_user)
        return render_template('search_game.html',
                               public_games=public_games,
                               private_games=private_games
                               )


class JoinGame(MethodView):
    def get(self, game_key):
        game = sketch_actions.get_game_by_key(game_key)

        # Check if private
        if game.perms == game.PRIVATE:
            if current_user.key() not in game.guests:
                abort(404)

        round = sketch_actions.get_latest_round(game.key())
        if round.round_type == round.SKETCH:
            return json.dumps('Story Page')
        else:
            return redirect(url_for('sketch'))





# class FilterGamesView(MethodView):
# 	def get(self):
# 		query = request.args.get("sSearch", "")
# 		if query:
# 			games = sketch_actions.guess_games_by_title(query)
# 		else:
# 			games = sketch_actions.get_latest_games(100)

# 		aaData = [[game.title, game.title, game.title ] for game in games ]

# 		return json.dumps({'aaData':aaData})


