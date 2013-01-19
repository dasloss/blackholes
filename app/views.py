from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash)
from flask.ext.login import (LoginManager, login_user, login_required,
                            current_user, logout_user)
from app.models import User
from app.forms import LoginForm, RegistrationForm, SettingsForm
import urllib, stripe, requests, os, json

login_manager = LoginManager()

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
@login_required
def index():
    return render_template('index.html',session=session)

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

@views.route('/pay/', methods=['GET', 'POST'])
@login_required
def pay():
    return render_template('pay.html', pubkey=PUBLISHABLE_KEY)

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
    stripe.Charge.create(
            amount='',                       
            currency="usd",
            card='',
            description=current_user.username +  "for x dollars"
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

@views.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', session=session), 404

@views.app_errorhandler(500)
def page_not_found(error):
    """Custom 500 page."""
    return render_template('500.html', session=session), 500
