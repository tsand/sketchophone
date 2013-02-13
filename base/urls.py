from base import views as base_views
from base import cron

def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
    app.add_url_rule('/about', view_func=base_views.AboutView.as_view('about'))
    
    # Cron jobs
    app.add_url_rule('/cron/<string:function>', view_func=base_views.Cron.as_view('cron'))
