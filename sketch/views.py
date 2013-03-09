import json

from flask import abort, redirect, url_for, request
from flask.views import MethodView
from flask.templating import render_template
from google.appengine.ext import db
from resources.flask_login import current_user
from sketch import actions as sketch_actions
from base import mail
from base import actions as base_actions


class SketchView(MethodView):
    def get(self):
        return render_template('sketch.html')

class CreationWizard(MethodView):
    def get(self):
        return render_template('/create_game/wizard.html',
                               current_user=current_user)

    def post(self):

        j_form = json.loads(request.data).get('form', None)

        title = str(j_form.get('name', 'foo'))
        created_by = str(j_form.get('created_by', 'Anonymous'))

        guests = [db.get(key) for key in j_form.get('guests', None)]
        guest_keys = [guest.key() for guest in guests]

        if j_form is not None:
            game, round = sketch_actions.create_game(
                first_round_text=str(j_form.get('start_text', '')),
                title=title,
                perms=str(j_form.get('perms', 'public')),
                guests=guest_keys,
                num_of_rounds=int(j_form.get('num_of_rounds', 3))
            )

            internal_game_link = url_for('game', game_key=game.key())
            external_game_link = url_for('game', game_key=game.key(),
                                         _external=True)
            for guest in guests:
                # Send email
                mail.send_created_game_email(guest.email,
                                             title,
                                             external_game_link,
                                             created_by)

                # Send notification

                base_actions.notify_user(
                    guest,
                    'New Game Request',
                    """
                    <strong>%s</strong> has invited you to play in the game <em>%s</em>
                    """ % (created_by, title),
                    internal_game_link)

            # For local debugging, since you can't send mail
            import logging
            logging.log(logging.INFO, 'GAME LINK: %s' % external_game_link)

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


class Game(MethodView):
    def get(self, game_key):
        game = sketch_actions.get_game_by_key(game_key)

        # Check if private
        if game.perms == game.PRIVATE:
            if current_user.key() not in game.guests:
                abort(404)

        round = sketch_actions.get_latest_round(game.key())
        if round.round_type == round.SKETCH:
            return json.dumps('Story page will go here')
        else:
            return render_template('sketch.html',
                                   game=game.title,
                                   story=round.data)

