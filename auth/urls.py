# this is where we handle our urls
# from here we associate what urls belong to what views that generate html or json ect..
# we call this method from the main.py

from auth import views as auth_views

def apply_urls(app):
    app.add_url_rule('/auth/user/', view_func=auth_views.User.as_view('user'))
    app.add_url_rule('/auth/register/', view_func=auth_views.Register.as_view('register'))
    app.add_url_rule('/auth/login/', view_func=auth_views.Login.as_view('login'))
    app.add_url_rule('/auth/logout/', view_func=auth_views.Logout.as_view('logout'))