from wtforms import Form, TextField, PasswordField, BooleanField, validators, ValidationError, TextAreaField, FileField, IntegerField
from flask.ext.login import current_user
from flask.ext.wtf import file_allowed, file_required
from flask.ext.uploads import UploadSet, IMAGES
from app.models import User, Candidate

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

images = UploadSet("images",IMAGES)

class CandidateForm(Form):
    candidatename = TextField('Candidate Name', [validators.Required()])
    electedoffice = TextField('Elected Office', [validators.Required()])
    maxdonation = IntegerField('Maximum Donation', [validators.Required()])
    bio = TextAreaField('Bio', [validators.Required()])
    website = TextField('Website', [validators.Required()])
    paymentkey = TextField('Stripe Key', [validators.Optional()])
    imgupload = FileField('Image File', validators = [file_required(),
                                       file_allowed(images, "Images only!")])
