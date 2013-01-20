from wtforms import Form, TextField, PasswordField, BooleanField, validators, IntegerField

class LoginForm(Form):
    username = TextField('User Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember me', [validators.Optional()])

class RegistrationForm(Form):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Required(), validators.Email()])
    username = TextField('User Name', [validators.Required()])
    password = PasswordField('New password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password', [validators.Required()])
    #accept_tos = BooleanField('I accept the ToS', [validators.Required()])

class SettingsForm(Form):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Required(), validators.Email()])
    old_password = PasswordField('Old password', [validators.Required()])
    password = PasswordField('Change password', [
        validators.Required(),
        validators.EqualTo('confirm', message='New passwords must match')
        ])
    confirm = PasswordField('Repeat password', [validators.Required()])

class EventForm(Form):
    name = TextField('Event Name', [validators.Required()])
    intervalMinutes = IntegerField('Length of Time', [validators.Required()])
    priority = IntegerField('Priority', [validators.Required(),
                           validators.NumberRange(min=0, max=5, message=
                            "Priority must be between 0 and 5")])
    type = TextField('Type', [validators.Optional()])
