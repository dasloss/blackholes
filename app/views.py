from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash)
from flask.ext.login import (LoginManager, login_user, login_required,
                            current_user, logout_user)
from app.models import *
from app.forms import *
from app.settings import PUBLISHABLE_KEY, SECRETIVE_KEY, CLIENT_ID
import stripe
import urllib
import requests

login_manager = LoginManager()

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
@login_required
def index():
    candidates = User.objects(candidate=True)
    return render_template('index.html',candidates=candidates,session=session)

@views.route('/authorize/')
@login_required
def authorize():
  site   = 'https://connect.stripe.com/oauth/authorize'
  params = {'response_type': 'code',
            'scope': 'read_write',
            'client_id': CLIENT_ID
           }
  # Redirect to Stripe /oauth/authorize endpoint
  url = site + '?' + urllib.urlencode(params)
  return redirect(url)
 
@views.route('/oauth/callback/')
@login_required
def callback():
  code   = request.args.get('code')
  header = {'Authorization': 'Bearer %s' % SECRETIVE_KEY}
  data   = {'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'code': code
           }
  # Make /oauth/token endpoint POST request
  url ='https://connect.stripe.com/oauth/token'
  resp = requests.post(url, params=data, headers=header)
  # Grab access_token (use this as your user's API key)
  jsontoken = resp.json()#.get('access_token')
  token = jsontoken['access_token']
  current_user.set_token(token)
  current_user.connected = True
  current_user.save()
  return redirect(url_for('views.settings'))

@views.route('/about/')
def about():
    """Render about."""
    return render_template('about.html', session=session)

@views.route('/donate/', methods=['GET', 'POST'])
@login_required
def donate():
    return render_template('donate.html', pubkey=PUBLISHABLE_KEY)

@views.route('/charge/', methods=['GET', 'POST'])
@login_required
def charge():
    # set secret key, get the credit card details submitted by the form   
    stripe.api_key = SECRETIVE_KEY
    token = request.form['stripeToken']
    if current_user.stripe_customer_id == None:
        # create a Customer                                             
        customer = stripe.Customer.create(
            card=token,
            description=current_user.username
        )
        # save the customer ID in your database so you can use it later  
        current_user.set_stripe_customer_id(customer.id)
        current_user.save()
    # later retrieve id and charge each donation          
    customer_id = current_user.stripe_customer_id
    for recipient in recipients:
        chargetoken = stripe.Token.create(
            customer=customer_id,
            api_key=recipient.token # recipient's Stripe auth token
        )
        stripe.Charge.create(
            amount=recipient.amount,                       
            currency="usd",
            card=chargetoken,
            description=current_user.username + " to " + recipient.name
        )
    return render_template('charge.html')

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
    form = None
    candidate = current_user.is_candidate
    connected = current_user.is_connected
    if current_user.service == 'local':
        form = SettingsForm(request.form, email=current_user.email, name=current_user.name, electedoffice=current_user.electedoffice, maxdonation=current_user.maxdonation, bio=current_user.bio, website=current_user.website)
    if request.method == 'POST' and form.validate():
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.electedoffice = form.electedoffice.data
        current_user.maxdonation = form.maxdonation.data
        current_user.bio = form.bio.data
        current_user.website = form.website.data
        if form.password.data != None:
            current_user.set_password(form.password.data)
        current_user.save()
    return render_template('settings.html', form=form, candidate=candidate, connected=connected)

@views.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.authenticated = False
    current_user.save()
    logout_user()
    return redirect(url_for('views.index'))

@views.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.username == 'admin':
        users = User.objects
        class F(SelectionForm):
            pass
        for user in users:
            username = user.username
            setattr(F, username, BooleanField(username))
        form = F(request.form, username=user.candidate)
        if request.method == 'POST' and form.validate():
            for user in users:
                if user.username in request.form:
                    user.candidate = True
                else:
                    user.candidate = False
                user.save()
        return render_template('admin.html',users=users,form=form)
    else:
        flash("You are not an authorized administrator")
        return redirect(url_for('views.index'))

@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html', session=session), 404

@views.app_errorhandler(500)
def page_not_found(error):
    """Custom 500 page."""
    # Insert error logging here.
    return render_template('500.html', session=session), 500
