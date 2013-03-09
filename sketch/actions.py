from sketch import models as sketch_models
from google.appengine.ext import db



# You can run this from the interactive console on your local host
# http://localhost:8001/_ah/admin/interactive
"""
from sketch import actions
actions.create_test_data(100)
"""
def create_test_data(num = 100):
    import random
    for n in xrange(num):
        rand_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for abc in range(7))
        create_game('Mumble dog face to the banana patch.', rand_string, 'public',[], random.randint(2,100))


def create_game(first_round_text, title, perms, guests, num_of_rounds):
    new_game = sketch_models.Game(title = title,
                                perms = perms,
                                guests = guests,
                                number_of_rounds = num_of_rounds)
    new_game.put()
    new_round = add_round_by_game_key(new_game.key(), first_round_text, None)
    return new_game, new_round

def get_game_by_key(key):
    return db.get(key)

def get_game_by_title(title):
    return sketch_models.Game.all().filter('title =',title).get()

def get_latest_games(num = None, offset = 0):
    return sketch_models.Game.all().order("-created").fetch(num, offset = offset)

def get_latest_round(game_key):
    latest_round = sketch_models.Round.all().ancestor(game_key).order("-created").get()
    return latest_round

def get_rounds_by_game_key(game_key, num = None, offset = 0):
    return sketch_models.Round.all().ancestor(game_key).order("-created").fetch(num, offset = offset)

def get_latest_public_games(num=None, offset=0):
    return sketch_models.Game.all().filter('perms =', 'public').order("-created").fetch(num, offset = offset)

def get_private_games(user, num=None, offset=0):
    all_games = sketch_models.Game.all().filter('perms =', 'private').order("-created").fetch(num, offset = offset)
    user_games = []
    for game in all_games:
        if user.key() in game.guests:
            user_games.append(game)
    return user_games



def add_round_by_game_key(game_key, new_data, participant):
    game = get_game_by_key(game_key)
    last_round = get_latest_round(game_key)
    if last_round is not None:
        new_round_type = sketch_models.Round.SKETCH if last_round.round_type == sketch_models.Round.TEXT else sketch_models.Round.TEXT
    else:
        new_round_type = sketch_models.Round.TEXT

    new_round = sketch_models.Round(data = new_data,
                                    user = participant,
                                    round_type = new_round_type,
                                    parent = game)
    new_round.put()
    return new_round

def guess_games_by_title(title):
    games = sketch_models.Game.all().filter('title >=', title).filter('title <', title + u'\ufffd')
    return games


