import random
from datetime import datetime, timedelta
from google.appengine.ext import db

from auth import models as auth_models
from auth import utils as auth_utils

from base import models as base_models

from sketch import actions as sketch_actions
from sketch import models as sketch_models


def delete_expired_users():
    """
    Deletes users who signed up but did not register within 24 hours
    """
    users = auth_models.User.all().filter('registered =', False).run()
    expiry_time = datetime.now() - timedelta(1)
    for user in users:
        if user.created < expiry_time:
            user.delete()


def reset_data_store():
    """
    Removes all models from the datastore
    """
    to_delete = []
    to_delete.extend(sketch_models.Game.all(keys_only=True).fetch(None))
    to_delete.extend(sketch_models.Round.all(keys_only=True).fetch(None))
    to_delete.extend(auth_models.User.all(keys_only=True).fetch(None))
    to_delete.extend(base_models.Notification.all(keys_only=True).fetch(None))
    db.delete(to_delete)


def create_registered_user(username, password):
    """
    Creates a registered user for testing purposes
    """
    password, salt = auth_utils.salt_password(password)
    user = auth_models.User(
        username=username,
        password=password,
        salt=salt,
        email='%s@test.com' % username,
        registered=True
    )
    user.put()
    return user


def generate_random_users(count=25):
    """
    Generates random test users
    """
    for n in xrange(count):
        rand_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for abc in range(7))
        create_registered_user(rand_string, 'pwd')


def create_test_game(game_name, num_rounds, user=None):
    """
    Create a test game
    """
    if user is None:
        user = create_registered_user('TEST_LOADER', 'test')

    game = sketch_actions.create_game('Round #0', game_name, 'public', num_rounds, user)

    sketch_json = '{"aspectRatio":2,"strokes":[{"stroke":[{"x":0,"y":0,"type":"mousedown"},{"x":1,"y":1,"type":"mousemove"}],"color":"black","size":10}]}'

    for n in xrange(num_rounds):
        if n % 2 == 0:
            sketch_actions.add_round_by_game_key(game.key(), 'sketch', sketch_json, user)
        else:
            sketch_actions.add_round_by_game_key(game.key(), 'story', 'Round #%s' % n, user)

    print 'The Game Key ---> %s' % (game.key())


def create_test_data(num_games=5, rounds_per_game=100):
    """
    Create test data
    """
    user = create_registered_user('TEST_LOADER', 'test')

    for n in xrange(num_games):
        rand_string = ''.join(
            random.choice('abcdefghijklmnopqrstuvwxyz') for abc in range(7))
        create_test_game(rand_string, rounds_per_game, user)



