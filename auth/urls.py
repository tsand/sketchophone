# this is where we handle our urls
# from here we associate what urls belong to what views that generate html or json ect..
# we call this method from the main.py
from auth import views as auth_views

def apply_urls(app):
    app.add_url_rule('/user/', view_func=auth_views.UserView.as_view('user'))