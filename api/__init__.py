import os
import time
from werkzeug.exceptions import NotFound
from werkzeug.wsgi import DispatcherMiddleware, SharedDataMiddleware
from flask import Flask, jsonify

from api.models import init_db, db_session

init_db()
flask_app = Flask(__name__, static_folder='../src', static_url_path='')
flask_app.secret_key = 'notreallythatsecret'

from api.controllers.user import user_bp

flask_app.register_blueprint(user_bp)

@flask_app.teardown_appcontext
def cleanup_db_session(exc=None):
    db_session.remove()

@flask_app.route('/')
def root():
    return flask_app.send_static_file('index.html')
