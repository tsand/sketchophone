from sketch import views as sketch_views


def apply_urls(app):
    app.add_url_rule('/game/search/', view_func=sketch_views.SearchGamesView.as_view('search'))
    app.add_url_rule('/game/create', view_func=sketch_views.CreationWizard.as_view('wizard'))
    app.add_url_rule('/game/<game_key>', view_func=sketch_views.Game.as_view('game'))
    app.add_url_rule('/game/sketch/<game_key>', view_func=sketch_views.Game.as_view('game'))
    app.add_url_rule('/game/edit/<game_key>', view_func=sketch_views.EditGame.as_view('edit_game'))
    app.add_url_rule('/game/timeline/<game_key>', view_func=sketch_views.Timeline.as_view('timeline'))
    app.add_url_rule('/game/evict/<game_key>', view_func=sketch_views.Evict.as_view('evict'))
    app.add_url_rule('/game/success', view_func=sketch_views.SuccessView.as_view('success'))
    app.add_url_rule('/game/examine/<round_key>', view_func=sketch_views.ExamineView.as_view('examine'))
    app.add_url_rule('/game/flag', view_func=sketch_views.FlagView.as_view('flag_round'))
    app.add_url_rule('/game/ban', view_func=sketch_views.BanView.as_view('ban_round'))
    app.add_url_rule('/game/end', view_func=sketch_views.EndGameView.as_view('end_game'))


