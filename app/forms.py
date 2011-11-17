from wtforms import Form, TextField, PasswordField, BooleanField, validators, ValidationError
from app.models import User

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember me', [validators.Optional()])

class RegistrationForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=3, max=20)])
    email = TextField('Email', [validators.Required(), validators.Email()])
    password = PasswordField('New password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password', [validators.Required()])
    #accept_tos = BooleanField('I accept the ToS', [validators.Required()])
