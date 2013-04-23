import random

from datetime import datetime, timedelta
from flask import url_for
from google.appengine.ext import db

from base import actions as base_actions
from sketch import models as sketch_models


def create_game(first_round_text, title, perms, max_rounds, created_by):
    # Store game model
    new_game = sketch_models.Game(title=title,
                                  perms=perms,
                                  max_rounds=max_rounds,
                                  num_rounds=0,
                                  created_by=created_by)
    new_game.put()

    # Attach game to created_by user
    created_by.attach_game(new_game.key())

    # Add 1st round
    add_round_by_game_key(new_game.key(), sketch_models.Round.STORY, first_round_text, created_by)
    return new_game


def get_game_by_key(key):
    """
    Given a game_key, return a game
    """
    return db.get(key)


def get_round_by_key(key):
    return db.get(key)


def get_game_by_title(title):
    """
    Return a game with a matching title
    """
    return sketch_models.Game.all().filter('title =', title).get()


def evict_user_by_game_key(key):
    game = get_game_by_key(key)
    if game is not None:
        game.evict_occupancy()
        game.put()
    return game


def evict_lazy_users():
    games = sketch_models.Game.all().filter('occupied_session !=', None).run()
    expiry_time = datetime.now() - timedelta(hours=3)

    to_put = []
    for game in games:
        if game.date_occupied < expiry_time:
            game.evict_occupancy()
            to_put.append(game)
    db.put(to_put)


def get_latest_round(game_key):
    """
    Given a game key, return the last round played in the game.
    """
    latest_round = sketch_models.Round.all().ancestor(game_key).order("-created").get()
    return latest_round


def get_oldest_rounds_by_game_key(game_key, num=None, offset=0):
    """
    Given a game key, get all rounds in the game
    """
    return sketch_models.Round.all().ancestor(game_key).order("created").fetch(num, offset=offset)


def get_latest_rounds_by_game_key(game_key, num=None, offset=0):
    """
    Given a game key, get all rounds in the game
    """
    return sketch_models.Round.all().ancestor(game_key).order("-created").fetch(num, offset=offset)


def get_latest_public_games(num=None, offset=0):
    """
    Return the public games.
    If not num, return all games
    """
    return sketch_models.Game.all().filter('perms =', 'public').order("-created").fetch(num, offset=offset)


def add_round_by_game_key(game_key, round_type, new_data, participant, session=None):
    """
    Add a round to a game
    """
    new_round = None
    game = get_game_by_key(game_key)
    if game is not None:

        # Quick hack fix because anons can't be stored in game model
        if participant.is_authenticated():
            participant = db.get(participant.key())
        else:
            participant = None

        new_round = sketch_models.Round(data=new_data,
                                        user=participant,
                                        round_type=round_type,
                                        parent=game)
        if new_round is not None:
            freed_user_key = game.updated_locked_users(participant, session)

            if freed_user_key:
                # Notify released user
                base_actions.notify_user(
                    db.get(db.Key(freed_user_key)),
                    'Your turn to play!',
                    'You may now return to the game %s' % game.title,
                    url_for('game', game_key=game.key()))

            new_round.put()
            game.num_rounds += 1

        game.evict_occupancy()
        game.put()

    return new_round

def ban_round_by_key(round_key, ban_state):
    round_to_ban = get_round_by_key(round_key)
    if round_to_ban is not None:
        round_to_ban.is_banned = ban_state
        round_to_ban.put()
        return True
    return False


def get_flagged_rounds(num=None, offset=0):
    return sketch_models.Round.all().filter('is_flagged =', True).filter('is_banned', False).fetch(num, offset=offset)


def flag_round_by_key(round_key, flag_state):
    round_to_flag = get_round_by_key(round_key)
    if round_to_flag is not None:
        round_to_flag.is_flagged = flag_state
        round_to_flag.put()
        return True
    return False


def guess_games_by_title(title):
    """
    Given a partial title, guess the game
    """
    games = sketch_models.Game.all().filter('title >=', title).filter('title <', title + u'\ufffd')
    return games
