from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import *
from app.forms import *

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
def index():
    """Render index."""
    return render_template('index.html', session=session)

@views.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data,
                    name=form.name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        return redirect('/')
    return render_template('register.html', form=form, session=session)

@views.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u"Username and password do not match")
            return redirect(url_for('views.login'))
        flash(u"Successfully logged in as %s" % user.username)
        session['username'] = user.username
        return redirect(url_for('views.index'))
    return render_template('login.html', form=form, session=session)

@views.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
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
