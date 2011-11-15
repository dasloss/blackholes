from flask import Flask, session
from flaskext.login import LoginManager
import settings
from mongoengine import connect
from views import views
from models import *

connect(settings.db, host=settings.db_host, port=settings.db_port, username=settings.db_user, password=settings.db_pass)

app = Flask(__name__, static_folder='../static', template_folder='../template')
app.config.from_object(settings)
app.register_blueprint(views)
app.secret_key = settings.secret_key

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(username):
    return User.objects.filter(username=username).first()

login_manager.login_view = "views.login"

if __name__ == "__main__":
    app.run()
