import random

from google.appengine.ext import db
from sketch import models as sketch_models
from auth import actions as auth_actions


def create_game(first_round_text, title, perms, num_of_rounds, created_by):
    # Store game model
    new_game = sketch_models.Game(title=title,
                                  perms=perms,
                                  number_of_rounds=num_of_rounds,
                                  created_by=created_by)
    new_game.put()

    # Attach game to created_by user
    created_by.attach_game(new_game.key())

    # Add 1st round
    add_round_by_game_key(new_game.key(), first_round_text, None)
    return new_game


def get_game_by_key(key):
    """
    Given a game_key, return a game
    """
    return db.get(key)


def get_game_by_title(title):
    """
    Return a game with a matching title
    """
    return sketch_models.Game.all().filter('title =', title).get()


def get_latest_round(game_key):
    """
    Given a game key, return the last round played in the game.
    """
    latest_round = sketch_models.Round.all().ancestor(game_key).order("-created").get()
    return latest_round


def get_rounds_by_game_key(game_key, num=None, offset=0):
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


def get_random_game():
    """
    Return the public games.
    If not num, return all games
    """
    game_count = sketch_models.Game.all(keys_only=True).filter('perms =', 'public').count()
    if game_count:
        rand_num = random.randint(0, game_count - 1)
        game = sketch_models.Game.all().filter('perms =', 'public').fetch(1, offset=rand_num)[0]
        return game
    return None


def add_round_by_game_key(game_key, new_data, participant):
    """
    Add a round to a game
    """
    game = get_game_by_key(game_key)
    last_round = get_latest_round(game_key)
    if last_round is not None:
        new_round_type = sketch_models.Round.SKETCH if last_round.round_type == sketch_models.Round.TEXT else sketch_models.Round.TEXT
    else:
        new_round_type = sketch_models.Round.TEXT

    new_round = sketch_models.Round(data=new_data,
                                    user=participant,
                                    round_type=new_round_type,
                                    parent=game)
    new_round.put()
    return new_round


def guess_games_by_title(title):
    """
    Given a partial title, guess the game
    """
    games = sketch_models.Game.all().filter('title >=', title).filter('title <', title + u'\ufffd')
    return games


# TEST FUNCTIONS
def create_test_data(num=100):
    """
    You can run this from the interactive console on your local host
    http://localhost:8001/_ah/admin/interactive
    -----
    from sketch import actions
    actions.create_test_data(100)
    """
    user = auth_actions.create_registered_user('TEST_LOADER', 'test')

    import random
    for n in xrange(num):
        rand_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for abc in range(7))

        game = create_game('Mumble dog face to the banana patch.',
                    rand_string,
                    'public',
                    random.randint(3, 100),
                    user)


