from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash)
from flask.ext.login import (LoginManager, login_user, login_required,
                            current_user, logout_user)
from app.models import User
from app.forms import LoginForm, RegistrationForm, SettingsForm
from settings import CLIENT_ID, CLIENT_SECRET, DEVELOPER_KEY
from oauth2client.client import OAuth2WebServerFlow 
from oauth2client.file import Storage
from apiclient.discovery import build
import httplib2

login_manager = LoginManager()

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                  client_secret=CLIENT_SECRET,
                  scope='https://www.googleapis.com/auth/calendar',
                  redirect_uri='http://localhost:5000/oauth/callback')

@views.route('/')
@login_required
def index():
    if current_user.connected:
        storage = Storage('credentials/'+current_user.username)
        credentials = storage.get()
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build(serviceName='calendar', version='v3', http=http,
                        developerKey=DEVELOPER_KEY)
        try:
            request = service.events().list(calendarId='primary')
            while request != None:
                response = request.execute()
                for event in response.get('items', []):
                    print repr(event.get('summary', 'NO SUMMARY')) + '\n'
                request = service.events().list_next(request, response)
        except AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-runthe application to re-authorize')
    else:
        flash("Please connect a google calendar.")
        redirect(url_for('views.settings'))
    return render_template('index.html',session=session)

@views.route('/about/')
def about():
    """Render about."""
    return render_template('about.html', session=session)

@views.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if not User.objects.filter(username=form.username.data):
            user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        service='local')
            user.set_password(form.password.data)
            user.authenticated = True
            user.save()
            login_user(user)
            flash("You successfully registered.")
            return redirect(url_for('views.index'))
        else:
            flash("That username is already taken.")
    return render_template('register.html', form=form, session=session)

@views.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(username=form.username.data).first()
        if user:
            good_password = user.check_password(form.password.data)
            if good_password:
                user.authenticated = True
                user.save()
                remember = request.form.get("remember", "n") == "y"
                if login_user(user, remember=remember):
                    flash("You logged in successfully.")
                    return redirect(url_for('views.index'))
                else:
                    flash("Your account is marked as inactive.")
            else:
                flash("There was an error logging in, password incorrect.")
        else:
            flash("There was an error logging in, user not found.")
    return render_template('login.html', form=form, session=session)

@views.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = None
    if current_user.service == 'local':
        form = SettingsForm(request.form, current_user)
    if request.method == 'POST' and form.validate():
        current_user.email = form.email.data
        current_user.name = form.name.data
        if form.password.data != None:
            current_user.set_password(form.password.data)
            flash("You updated your password.")
        current_user.save()
        flash("You updated your settings.")
    return render_template('settings.html', form=form)

@views.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.authenticated = False
    current_user.save()
    logout_user()
    flash("You logged out successfully.")
    return redirect(url_for('views.login'))

@views.route('/authorize/')
@login_required
def authorize():
    url = flow.step1_get_authorize_url()
    return redirect(url)

@views.route('/oauth/callback/')
@login_required
def callback():
    code = request.args.get('code')
    if code:
        credentials = flow.step2_exchange(code)
        storage = Storage('credentials/'+current_user.username)
        storage.put(credentials)
        current_user.connected = True
        current_user.save()
        flash("You connected to Google Calendar.")
    else: 
        error = request.args.get('error')
        flash("Connecation failed because: "+error)
    return redirect(url_for('views.settings'))

@views.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', session=session), 404

@views.app_errorhandler(500)
def page_not_found(error):
    """Custom 500 page."""
    return render_template('500.html', session=session), 500
