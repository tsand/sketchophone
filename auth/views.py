# This is where we generate the html data and or json

import json

from flask.views import MethodView
from flask.templating import render_template
from flask import request, redirect, url_for, flash

from lib.flask_login import login_user

from auth import models as auth_models
from auth import forms as auth_forms
from auth import utils as auth_utils
from auth import actions as auth_actions

class Login(MethodView):
    def get(self):
        form = auth_forms.LoginForm()
        return render_template("auth/login.html", form=form)

    def post(self):
        form = auth_forms.LoginForm()

        if form.validate_on_submit():
            if auth_utils.authenticate(form.email.data, form.password.data):
                user = auth_models.User.all().filter('email =', form.email.data).fetch(1)[0]
                flash('Success: User successfully logged in')
                return redirect(url_for('user'))
            else:
                flash('Error: Invalid Credentials')
        else:
            flash('Error: Incomplete Form')

        return redirect(url_for('login'))




class Register(MethodView):
    def get(self):
        form = auth_forms.RegisterForm()
        return render_template("auth/register.html", form=form)

    def post(self):
        form = auth_forms.RegisterForm()

        if form.validate_on_submit():
            if auth_actions.check_username_exists(form.username.data):
                new_user = auth_models.User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
                new_user.put()
                flash('Success: User Created')
                return redirect(url_for('user'))
            else:
                flash('Error: Username Already Exists')
        else:
            flash('Error: Incomplete Form')

        return redirect(url_for('register'))

class User(MethodView):
    # get is called when we want to get html data or json when the url
    # that is assigned to it is called
    def get(self):
        context = {}

        # request args gets the url arguments
        # for example if we go to the url http://localhost:8001/user/?name=Jack
        # we can get the data stored after the question mark
        # so if we want the variable stored in name we can use this method

        # if the argument doesn't exist, for example the url http://localhost:8001/user/
        # we use the default value 'John' that is explicitly defined here
        context['name'] = request.args.get('name', 'John')

        # now we can pass the name we found from our url and pass it to our render
        # tool that replaces the {{name}} in user.html with the name we want!
        return render_template('auth/user.html',  **context)