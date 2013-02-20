from sketch import models as sketch_models
from google.appengine.ext import db



def create_game(first_round_text, title, perms, guests, number_of_rounds):
	new_game = sketch_models.Game(title = title, 
								perms = perms, 
								guests = guests,
								number_of_rounds = number_of_rounds)
	new_game.put()
	new_round = add_round_by_game_key(new_game.key(), first_round_text, None)
	return new_game, new_round

def get_game_by_key(key):
	return db.get(key)

def get_game_by_title(title):
	return sketch_models.Game.all().filter('title =',title).get()

def get_latest_round(game_key):
	latest_round = sketch_models.Round.all().ancestor(game_key).order("-created").get()
	return latest_round

def get_rounds_by_game_key(game_key, num = None, offset = 0):
	return sketch_models.Round.all().ancestor(game_key).order("-created").fetch(num, offset = offset)

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



