import time
from werkzeug.exceptions import NotFound
from werkzeug.wsgi import DispatcherMiddleware
from flask import Flask, jsonify

from api.models import init_db, db_session

init_db()
flask_app = Flask(__name__)
flask_app.secret_key = 'notreallythatsecret'

from api.controllers.user import user_bp

flask_app.register_blueprint(user_bp)

@flask_app.teardown_appcontext
def cleanup_db_session(exc=None):
    db_session.remove()

app = DispatcherMiddleware(NotFound, {
    '/api': flask_app
})

if __name__ == '__main__':
    flask_app.run('0.0.0.0', 5000, debug=True)