from base import views as base_views


def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
    app.add_url_rule('/about', view_func=base_views.AboutView.as_view('about'))
    app.add_url_rule('/instructions', view_func=base_views.InstructionsView.as_view('instructions'))
    app.add_url_rule('/app', view_func=base_views.AppsView.as_view('app'))

    # Cron jobs
    app.add_url_rule('/cron/<string:function>', view_func=base_views.Cron.as_view('cron'))
