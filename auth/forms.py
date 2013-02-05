from lib.flask_wtf import Form, TextField, PasswordField, BooleanField, SubmitField
from lib.flask_wtf import Required, Email, EqualTo, ValidationError

from auth import actions as auth_actions

class RegisterForm(Form):

    username = TextField('Username', [Required()])
    email = TextField('Email', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    password_confirm = PasswordField('Confirm Password', [Required()])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')

#    def validate_username(self, field):
#        if auth_actions.check_username_exists(field):
#            raise ValidationError, "Username not available"


class LoginForm(Form):

    email = TextField('Email', [Required(message='Email')])
    password = PasswordField('Password', [Required(message='Pass')])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')
