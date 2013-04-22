import json

from base import mail
from base import actions as base_actions
from google.appengine.ext.db import Key
from flask import abort, url_for, request, flash, redirect
from flask.views import MethodView
from flask.templating import render_template
from resources.flask_login import current_user, login_required
from sketch import actions as sketch_actions
from sketch import forms as sketch_forms
from auth import actions as auth_actions


class Game(MethodView):
    def get(self, game_key):

        if not game_key:
            return redirect('/')

        game = sketch_actions.get_game_by_key(game_key)

        session = request.cookies.get('session')

        # Allow admins to override locked games
        if not current_user.is_authenticated() or not current_user.administrator:
            if game.is_locked_out(current_user, session):
                flash('You have to wait before you get to participate in this game again.')
                return redirect('/')

            if game.is_occupied() and not game.session_is_occupant(session):
                flash('Another user is currently completing a round in this game.')
                return redirect('/')

        game.occupy(current_user, session)
        game.put()

        # Check if private
        if game.perms == game.PRIVATE:
            if game.key() not in current_user.games:
                abort(404)

        round = sketch_actions.get_latest_round(game.key())
        if round.round_type == round.SKETCH:
            test = round.data
            return render_template('story.html',
                                   game=game,
                                   sketch_json=round.data)
        else:
            return render_template('sketch.html',
                                   game=game,
                                   story=round.data)

    def post(self, game_key):
        json_data = json.loads(request.data)
        session = request.cookies.get('session')

        game = sketch_actions.get_game_by_key(game_key)

        round_type = json_data.get('round_type', None)
        data = json_data.get('data', None)

        new_round = sketch_actions.add_round_by_game_key(game_key,
                                                         round_type,
                                                         data,
                                                         current_user,
                                                         session)

        current_user.attach_game(game.key())
        flash('%s Saved' % round_type.capitalize(), 'success')

        return redirect(url_for('success'))


class Timeline(MethodView):
    def get(self, game_key):
        game = sketch_actions.get_game_by_key(game_key)

        return render_template('timeline.html', game=game)

    def post(self, game_key):
        load_form = json.loads(request.data)
        number = load_form.get('number')
        offset = load_form.get('offset')

        rounds = sketch_actions.get_oldest_rounds_by_game_key(Key(game_key), number, offset)

        round_data = [{'data':r.get_data(), 'round_type':r.round_type, 'key':str(r.key())} for r in rounds]

        return json.dumps({'rounds': round_data})


class CreationWizard(MethodView):
    @login_required
    def get(self):
        return render_template('/create_game.html',
                               current_user=current_user)

    @login_required
    def post(self):
        form = json.loads(request.data).get('form', None)

        title = str(form.get('name', 'foo'))
        created_by = auth_actions.get_user_by_key(current_user.key())
        friends = dict(form.get('friends', {}))
        friends = [auth_actions.get_user_by_key(key) for key in friends.values()]

        if form is not None:
            game = sketch_actions.create_game(
                first_round_text=str(form.get('start_text', '')),
                title=title,
                perms=str(form.get('perms', 'public')),
                max_rounds=int(form.get('num_of_rounds', 3)),
                created_by=created_by
            )

            internal_game_link = url_for('game', game_key=game.key())
            external_game_link = url_for('game', game_key=game.key(), _external=True)
            for friend in friends:

                # Send email
                mail.send_created_game_email(friend.email,
                                             title,
                                             external_game_link,
                                             created_by.display_name)

                # Send notification
                base_actions.notify_user(
                    friend,
                    'New Game Request',
                    """
                    <strong>%s</strong> has invited you to play in the game <em>%s</em>
                    """ % (created_by.display_name, title),
                    internal_game_link
                )

                # Attach game to user
                friend.attach_game(game.key())

            # For local debugging, since you can't send mail
            import logging
            logging.log(logging.INFO, 'GAME LINK: %s' % external_game_link)

            flash('Game Created', 'success')

            return json.dumps({'success': True})
        return json.dumps({'success': False})


class EditGame(MethodView):
    def get(self, game_key):
        game = sketch_actions.get_game_by_key(game_key)
        if current_user.key() == game.created_by.key() or current_user.administrator:
            form = sketch_forms.EditGameForm()
            return render_template('edit_game.html', form=form, game=game)
        else:
            flash('Only the creator of the game may edit it')
            return redirect(url_for('user') + '#games')

    def post(self, game_key):
        if game_key:
            game = sketch_actions.get_game_by_key(game_key)
        else:
            return abort(404)

        if current_user.key() == game.created_by.key() or current_user.administrator:
            form = sketch_forms.EditGameForm()

            if form.validate_on_submit():
                game.title = form.name.data
                game.max_rounds = form.rounds.data
                game.perms = form.type.data
                game.put()
            else:
                # Show error messages
                for field in form.errors:
                    for error in form.errors[field]:
                        flash(error, 'error')
                return redirect('game/edit/' + game_key)

            flash('Game Updated')
            return redirect(url_for('user') + '#games')

        else:
            flash('Only the creator of the game may edit it')
            redirect(url_for('home'))


class SuccessView(MethodView):
    def get(self):
        return render_template('submition_success.html')


class SearchGamesView(MethodView):
    def get(self):
        public_games = sketch_actions.get_latest_public_games()
        session = request.cookies.get('session')
        for game in public_games:
            game.status = 'Available'
            
            if game.is_locked_out(current_user, session):
                game.status = 'Temporarily Locked Out'
            elif game.session_is_occupant(session):
                game.status = 'Currently Participating'
            elif game.is_occupied():
                game.status = 'Waiting on User'

        return render_template('search_game.html',
                               public_games=public_games)


class Evict(MethodView):
    def get(self, game_key):
        game = sketch_actions.get_game_by_key(game_key)

        if current_user.key() == game.created_by.key() or current_user.administrator:
            if game.is_occupied():
                game.evict_occupancy()
                flash('User Evicted', 'info')
            else:
                flash('The game is not currently occupied', 'info')
        else:
            flash('Only the creator of the game may evict users', 'error')

        return redirect(url_for('user') + '#games')

