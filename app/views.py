from flask import Blueprint, render_template, request, redirect, url_for
from app.models import *
from app.forms import *

views = Blueprint('views', __name__, static_folder='../static',
                  template_folder='../templates')

@views.route('/')
def index():
    """Render index."""
    return render_template('index.html')
