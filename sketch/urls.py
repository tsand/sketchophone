from sketch import views as sketch_views

def apply_urls(app):
    app.add_url_rule('/sketch/', view_func=sketch_views.SketchView.as_view('sketch'))
    app.add_url_rule('/sketch/create/', view_func=sketch_views.CreationWizard.as_view('wizard'))
    app.add_url_rule('/sketch/search/', view_func=sketch_views.SearchGamesView.as_view('search'))
    app.add_url_rule('/game/<game_key>', view_func=sketch_views.Game.as_view('game'))
    # app.add_url_rule('/sketch/filter/', view_func=sketch_views.FilterGamesView.as_view('filter_games'))
