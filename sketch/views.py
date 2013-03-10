import json

from base import mail
from base import actions as base_actions
from flask import abort, url_for, request, flash, redirect
from flask.views import MethodView
from flask.templating import render_template
from google.appengine.ext import db
from resources.flask_login import current_user, login_required
from sketch import actions as sketch_actions


class Game(MethodView):
    def get(self, game_key):

        if game_key:
            game = sketch_actions.get_game_by_key(game_key)
        else:
            # Return random game (oldest)
            game = sketch_actions.get_random_game()
            if not game:
                flash('No games avaliable')
                return redirect('/')

        # Check if private
        if game.perms == game.PRIVATE:
            if game.key() not in current_user.games:
                abort(404)

        round = sketch_actions.get_latest_round(game.key())
        if round.round_type == round.SKETCH:
            return json.dumps('Story page will go here')
        else:
            return render_template('sketch.html',
                                   game=game.title,
                                   story=round.data)



class CreationWizard(MethodView):
    @login_required
    def get(self):
        return render_template('/create_game/wizard.html',
                               current_user=current_user)

    @login_required
    def post(self):

        j_form = json.loads(request.data).get('form', None)

        title = str(j_form.get('name', 'foo'))

        guests = [db.get(key) for key in j_form.get('guests', None)]
        guest_keys = [guest.key() for guest in guests]

        created_by = str(j_form.get('created_by'))
        if created_by:
            created_by = db.get(created_by)

            # Add created_by user to game
            guest_keys.append(created_by.key())

        if j_form is not None:
            game = sketch_actions.create_game(
                first_round_text=str(j_form.get('start_text', '')),
                title=title,
                perms=str(j_form.get('perms', 'public')),
                num_of_rounds=int(j_form.get('num_of_rounds', 3)),
                created_by=created_by
            )

            internal_game_link = url_for('game', game_key=game.key())
            external_game_link = url_for('game', game_key=game.key(),
                                         _external=True)
            for guest in guests:

                # Send email
                mail.send_created_game_email(guest.email,
                                             title,
                                             external_game_link,
                                             created_by.display_name)

                # Send notification
                base_actions.notify_user(
                    guest,
                    'New Game Request',
                    """
                    <strong>%s</strong> has invited you to play in the game <em>%s</em>
                    """ % (created_by.display_name, title),
                    internal_game_link
                )

                # Attach game to user
                guest.attach_game(game.key())

            # For local debugging, since you can't send mail
            import logging
            logging.log(logging.INFO, 'GAME LINK: %s' % external_game_link)

            return json.dumps({'success': True})
        return json.dumps({'success': False})


class SearchGamesView(MethodView):
    def get(self):
        public_games = sketch_actions.get_latest_public_games()
        return render_template('search_game.html',
                               public_games=public_games)

