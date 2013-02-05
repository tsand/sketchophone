from lib.flask_wtf import Form, TextField, PasswordField, BooleanField, SubmitField
from lib.flask_wtf import Required, Email, EqualTo, Length, ValidationError

from auth import actions as auth_actions

import settings

class RegisterForm(Form):
    # Error messages
    required = '%s required'
    password_length = 'Password must be %s characters' % settings.PASSWORD_LENGTH
    password_match = 'Passwords must match'

    # Fields
    username = TextField('Username', [Required(message=required % 'Username')])
    email = TextField('Email', [Required(message=required % 'Email'), Email()])
    password = PasswordField('Password', [Required(message=required % 'Password'),
                                          Length(settings.PASSWORD_LENGTH, message=password_length)])
    confirm = PasswordField('Confirm Password', [EqualTo('password', message=password_match)])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')

    def validate_username(self, field):
        if auth_actions.check_username(field.data):
            raise ValidationError, "Username not available"

    def validate_email(self, field):
        if auth_actions.check_email(field.data):
            raise ValidationError, "User already exists"

class LoginForm(Form):
    # Error messages
    required = '%s required'

    # Fields
    email = TextField('Email', [Required(message=required % 'Email')])
    password = PasswordField('Password', [Required(message=required % 'Password')])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')

