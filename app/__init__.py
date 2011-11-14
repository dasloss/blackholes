from flask import Flask, session
from views import views
import settings
from mongoengine import connect

connect(settings.db, host=settings.db_host, port=settings.db_port, username=settings.db_user, password=settings.db_pass)

app = Flask(__name__, static_folder='../static', template_folder='../template')
app.config.from_object(settings)
app.register_blueprint(views)

if __name__ == "__main__":
    app.run(debug=True)
