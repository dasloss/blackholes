from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flaskext.login import login_user, login_required, current_user, logout_user
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
