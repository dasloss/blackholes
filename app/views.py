from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash)
from flaskext.login import (LoginManager, login_user, login_required,
                            current_user, logout_user)
from flaskext.oauth import OAuth
from app.models import *
from app.forms import *

login_manager = LoginManager()

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',
    consumer_key='xBeXxg9lyElUgwZT6AZ0A',
    consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk'
)

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
def index():
    """Render index."""
    return render_template('index.html', session=session)

@twitter.tokengetter
def get_twitter_token():
    user = current_user
    if user.is_authenticated():
        return user.oauth_token, user.oauth_secret

@views.route('/auth/twitter/')
def auth_twitter():
    return twitter.authorize(callback=url_for('views.twitter_oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@views.route('/twitter-oauth-authorized')
@twitter.authorized_handler
def twitter_oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('views.index')
    if resp is None:
        flash(u"You denied the request to sign in.")
        return redirect(next_url)
    user = User.objects.filter(username=resp['screen_name']).first()
    if not user:
        user = User(username=resp['screen_name'],
                    service='twitter')
    if user.password is not None:
        flash('That username exists.') # TODO this is not robust; I should be
                                       # able to handle both a local account
                                       # "kobutsu" and a Twitter-auth'ed
                                       # account "kobutsu"
        return redirect(url_for('views.login'))
    user.oauth_token = resp['oauth_token']
    user.oauth_secret = resp['oauth_token_secret']
    user.authenticated = True
    user.save()
    login_user(user, remember=True)
    return redirect(next_url)

@views.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if not User.objects.filter(username=form.username.data):
            user = User(username=form.username.data,
                        email=form.email.data,
                        service='local')
            user.set_password(form.password.data)
            user.authenticated = True
            user.save()
            login_user(user)
            return redirect(request.args.get("next") or url_for('views.index'))
        else:
            flash("That username is already taken.")
    return render_template('register.html', form=form, session=session)

@views.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(username=form.username.data).first()
        if user:
            good_password= user.check_password(form.password.data)
            if good_password:
                user.authenticated = True
                user.save()
                remember = request.form.get("remember", "n") == "y"
                if login_user(user, remember=remember):
                    return redirect(request.args.get("next") or url_for('views.index'))
                else:
                    flash("Your account is marked as inactive.")
                    return redirect(url_for('views.login'))
            else:
                flash("There was an error logging in.")
        else:
            flash("There was an error logging in.")
        redirect(url_for('views.login'))
    return render_template('login.html', form=form, session=session)

@views.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    account_type = current_user.service
    return render_template('settings.html', account_type=account_type)

@views.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.authenticated = False
    current_user.save()
    logout_user()
    return redirect(url_for('views.index'))

@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html', session=session), 404

@views.app_errorhandler(500)
def page_not_found(error):
    """Custom 500 page."""
    # Insert error logging here.
    return render_template('500.html', error=error, session=session), 500
