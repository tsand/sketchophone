# This is where we generate the html data and or json

from flask.views import View, MethodView
from flask.templating import render_template
from flask import request, redirect, url_for, flash, session

from resources.flask_login import login_user, current_user, logout_user
from resources.flask_oauth import OAuth

from auth import models as auth_models
from auth import forms as auth_forms
from auth import utils as auth_utils
from auth import actions as auth_actions

import settings

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=settings.FACEBOOK_APP_ID,
    consumer_secret=settings.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


class Register(MethodView):

    def get(self):
        form = auth_forms.RegisterForm()
        return render_template("auth/register.html", form=form)

    def post(self):
        form = auth_forms.RegisterForm()

        # Validate form
        if form.validate_on_submit():

            # Salt password
            password, salt = auth_utils.salt_password(form.password.data)

            # Create new user
            new_user = auth_models.User(username=form.username.data,
                email=form.email.data,
                password=password,
                salt=salt)
            new_user.put()

            # Login as user
            login_user(new_user, remember=form.remember.data)

            # Redirect to User page
            flash('Registration Successful', 'success')
            return redirect(url_for('user'))

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

        # Stay on registration page
        return redirect(url_for('register'))


class Login(MethodView):

    def get(self):
        form = auth_forms.LoginForm()
        return render_template("auth/login.html", form=form)

    def post(self):
        form = auth_forms.LoginForm()

        # Validate Form
        if form.validate_on_submit():

            # Authenticate user
            if auth_actions.authenticate(form.username.data, form.password.data):

                # Login as user
                user = auth_models.User.all().filter('username =', form.username.data).fetch(1)[0]
                login_user(user, remember=form.remember.data)

                # Redirect to user page
                flash('Logged In', 'success')
                return redirect(url_for('user'))

            else:
                flash('Invalid Credentials', 'error')

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

        # Stay on login page
        return redirect(url_for('login'))


class Logout(View):

    def dispatch_request(self):
        logout_user()
        flash('You are logged out', 'info')
        return redirect(url_for('home'))


class User(View):

    def dispatch_request(self):
        return render_template('auth/user.html',  user=current_user)


class FacebookLogin(View):

    def dispatch_request(self):
        return facebook.authorize(callback=url_for('facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))


class FacebookAuthorized(View):

    @facebook.authorized_handler
    def dispatch_request(self, other):

        # Setting the oauth token in the session
        session['oauth_token'] = str(self.get('access_token', ''))

        # Receiving the user info from Facebook
        me = facebook.get('/me')

        # Connect facebook account to current user
        if current_user.is_authenticated():
            current_user.name = me.data['name']
            current_user.facebook_id = me.data['id']
            current_user.put()

        else:
            # Checking for the user associated with the user's facebook ID
            user = auth_actions.get_user_by_facebook_id(me.data['id'])

            # Log in with facebook user
            if user:
                login_user(user, True)

            # New Account
            else:
                user = auth_models.User(name=me.data['name'],
                    facebook_id=me.data['id'],
                    email=me.data['email'],
                    username=me.data['username'])
                user.put()

        return redirect(url_for('user'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token'), settings.FACEBOOK_APP_SECRET