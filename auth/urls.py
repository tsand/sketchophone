# this is where we handle our urls
# from here we associate what urls belong to what views that generate html or json ect..
# we call this method from the main.py

from auth import views as auth_views

def apply_urls(app):
    app.add_url_rule('/auth/user/', view_func=auth_views.User.as_view('user'))
    app.add_url_rule('/auth/register/', view_func=auth_views.Register.as_view('register'))
    app.add_url_rule('/auth/login/', view_func=auth_views.Login.as_view('login'))
    app.add_url_rule('/auth/logout/', view_func=auth_views.Logout.as_view('logout'))
    app.add_url_rule('/auth/password/', view_func=auth_views.ChangePassword.as_view('password'))

    # Facebook login
    app.add_url_rule('/auth/facebook_login', view_func=auth_views.FacebookLogin.as_view('facebook_login'))
    app.add_url_rule('/auth/facebook_auth', view_func=auth_views.FacebookAuthorize.as_view('facebook_auth'))
    app.add_url_rule('/auth/facebook_deauth', view_func=auth_views.FacebookDeauthorize.as_view('facebook_deauth'))
