import hashlib
from werkzeug.exceptions import Unauthorized, NotFound
from flask import Blueprint, jsonify, request, session

from api.utils import requires_authentication
from api.models import db_session, User
from api.schemas import UserSchema

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# TODO: Testing only, should connect to external user authentication system
@user_bp.route('/', methods=['POST'])
def create_user():
    j = request.get_json()
    u = User(first_name=j['first_name'],
             last_name=j['last_name'],
             username=j['username'],
             role=j['role'])

    # Hash password
    # This is not a secure way at all to do this...
    u.password_hash = hashlib.sha256(j['password'].encode()).hexdigest()

    db_session.add(u)
    db_session.commit()

    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_session.delete(User.query.get(user_id))
    db_session.commit()

    return jsonify(deleted=True)

@user_bp.route('/', methods=['GET'])
@requires_authentication()
def get_current_user():
    u = User.query.get(session['user_id'])
    if not u:
        raise Unauthorized('Not logged in.')

    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    u = User.query.get(user_id)
    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/login', methods=['POST'])
def login_user():
    j = request.get_json()
    u = User.query.filter(User.username == j['username'])\
        .filter(User.password_hash == hashlib.sha256(j['password'].encode()).hexdigest()).first()

    if not u:
        raise Unauthorized('Not allowed to access this site.')

    session['user_id'] = u.id

    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/logout', methods=['POST'])
def logout_user():
    session.pop('user_id')
    return jsonify(success=True)