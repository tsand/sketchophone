import json

from flask import request, redirect, url_for, flash, session
from flask.views import View, MethodView
from flask.templating import render_template

from resources.flask_login import login_user, current_user, logout_user, login_required

from auth import facebook
from auth import models as auth_models
from auth import forms as auth_forms
from auth import utils as auth_utils
from auth import actions as auth_actions

from base import mail

from sketch import actions as sketch_actions


class Register(MethodView):

    def get(self):
        verification = False
        form = auth_forms.RegisterForm()

        # If verifying account via email
        registration_id = request.args.get('id')
        if registration_id:

            # Check if user exists
            user = auth_actions.get_user_by_registration_id(registration_id)
            if user:

                # If already registered
                if user.is_registered():
                    return redirect(url_for('login'))

                # If not yet registered
                else:
                    form = auth_forms.RegisterVerificationForm()
                    verification = True

            # Ignore registration id
            else:
                return redirect(url_for('register'))

        return render_template("auth/register.html", form=form, verification=verification)

    def post(self):
        verification = False
        form = auth_forms.RegisterForm()

        # If verifying account via email
        registration_hash = request.args.get('id')
        if registration_hash:
            verification = True
            form = auth_forms.RegisterVerificationForm()

        # Validate form
        if form.validate_on_submit():

            if verification:

                # Find user by registration id
                registration_id = request.args.get('id')
                user = auth_actions.get_user_by_registration_id(registration_id)

                if user:

                    # Salt password
                    password, salt = auth_utils.salt_password(form.password.data)

                    # Update user info
                    user.username = form.username.data
                    user.password = password
                    user.salt = salt
                    user.registered = True
                    user.put()

                    # Login as user
                    login_user(user, remember=form.remember.data)

                    # Redirect to User page
                    flash('Registration Successful', 'success')
                    return redirect(url_for('user'))

                else:
                    return redirect(url_for('register'))

            else:

                # Generate registration ID
                registration_id = auth_utils.get_salt()
                registration_url = url_for('register', _external=True, id=registration_id)

                # Send registration email
                mail.send_registration_email(form.email.data, registration_url)

                # For local debugging, since you can't send mail
                import logging
                logging.log(logging.INFO, 'REGISTRATION URL: %s' % registration_url)

                # Delete unregistered user
                user = auth_actions.get_user_by_email(form.email.data)
                if user:
                    user.delete()

                # Create unregistered user
                new_user = auth_models.User(email=form.email.data, registration_id=registration_id)
                new_user.put()

                flash('An email was sent to verify your account', 'info')

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

        # Stay on registration page
        return redirect(url_for('register', id=registration_hash))


class Login(MethodView):

    def get(self):
        form = auth_forms.LoginForm()
        return render_template("auth/login.html", form=form)

    def post(self):
        form = auth_forms.LoginForm()

        # Validate Form
        if form.validate_on_submit():

            # Authenticate user
            if auth_actions.authenticate(form.email.data, form.password.data):

                # Login as user
                user = auth_models.User.all().filter('email =', form.email.data).fetch(1)[0]
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

    @login_required
    def dispatch_request(self):
        logout_user()
        flash('You are logged out', 'info')
        return redirect(url_for('home'))


class ChangePassword(MethodView):

    @login_required
    def get(self):
        form = auth_forms.ChangePasswordForm()
        return render_template("auth/password.html", form=form, user=current_user)

    @login_required
    def post(self):
        form = auth_forms.ChangePasswordForm()

        # Validate form
        if form.validate_on_submit():

            if auth_actions.authenticate(current_user.email, form.current_password.data):

                # Update password
                password, salt = auth_utils.salt_password(form.password.data)
                current_user.password = password
                current_user.salt = salt
                current_user.put()

                flash('Password change successful', 'success')
                return redirect(url_for('user'))

            else:
                flash('Current Password does not match', 'error')

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

        # Stay on registration page
        return redirect(url_for('password'))


class User(View):

    @login_required
    def dispatch_request(self):
        games = current_user.get_games()
        notifications = current_user.get_notifications()

        for game in games:
            game.last_updated = sketch_actions.get_latest_round(game.key()).created

        return render_template('auth/user.html',
                               games=games,
                               notifications=notifications)


class HandleUserQuery(MethodView):

    def get(self):
        query = request.args.get('query', '')
        users = auth_actions.guess_users_by_username(query)

        users = [{'username': user.username, 'key': str(user.key())} for user in users]
        return json.dumps({
            'users': filter(lambda user: user["username"] != current_user.username, users)
        })


class FacebookLogin(View):

    def dispatch_request(self):
        return facebook.authorize(callback=url_for('facebook_auth',
            next=request.args.get('next') or request.referrer or None, _external=True))


class FacebookAuthorize(View):

    @facebook.authorized_handler
    def dispatch_request(self, other):

        # Setting the oauth token in the session
        session['oauth_token'] = str(self.get('access_token', ''))

        # Receiving the user info from Facebook
        me = facebook.get('/me')

        # Connect facebook account to current user
        if current_user.is_authenticated():

            user = auth_actions.get_user_by_facebook_id(me.data['id'])

            # Check if facebook user has already registered
            if user:
                flash('Facebook user already has account')

            else:
                current_user.username = me.data['username']
                current_user.name = me.data['name']
                current_user.facebook_id = me.data['id']
                current_user.put()
                

        else:
            # Checking for the user associated with the user's facebook ID
            user = auth_actions.get_user_by_facebook_id(me.data['id'])

            # New Account
            if not user:

                # Check if there is already a user with that email
                if auth_actions.check_email(me.data['email']):
                    flash('There is already a user with that email')
                    return redirect(url_for('register'))

                # Create new user
                else:
                    user = auth_models.User(name=me.data['name'],
                                            username=me.data['username'],
                                            facebook_id=me.data['id'],
                                            email=me.data['email'],
                                            registered=True)
                    user.put()

            login_user(user, True)

        return redirect(url_for('user'))


class FacebookDeauthorize(View):

    @login_required
    def dispatch_request(self):
        current_user.facebook_id = None
        current_user.name = None
        current_user.put()
        return redirect(url_for('user'))


class Notifications(View):

    @login_required
    def dispatch_request(self):
        notes = current_user.get_notifications()
        notes = [(note.title, note.description) for note in notes]
        current_user.read_notifications()  # Mark as read
        return json.dumps(notes)

