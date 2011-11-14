from flask import Blueprint, render_template, request, redirect, url_for
from app.models import *
from app.forms import *

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
def index():
    """Render index."""
    return render_template('index.html')

@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@views.app_errorhandler(500)
def page_not_found(error):
    """Custom 500 page."""
    # Insert error logging here.
    return render_template('500.html'), 500
