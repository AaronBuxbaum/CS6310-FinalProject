import hashlib
from werkzeug.exceptions import Unauthorized
from flask import Blueprint, jsonify, request, session

from api.models import db_session, User
from api.schemas import UserSchema

user_bp = Blueprint('user', __name__, url_prefix='/user')

# TODO: Testing only, should connect to external user authentication system
@user_bp.route('/', methods=['POST'])
def create_user():
    user_data = UserSchema().load(request.get_json()).data
    u = User(first_name=user_data['first_name'],
             last_name=user_data['last_name'],
             username=user_data['username'],
             role=user_data['role'])

    # Hash password
    # This is not a secure way at all to do this...
    u.password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()

    db_session.add(u)
    db_session.commit()

    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_session.delete(User.query.get(user_id))
    db_session.commit()

    return jsonify(deleted=True)

@user_bp.route('/', methods=['GET'])
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
    r = request.get_json()
    u = User.query.filter(User.username == r.get('username'))\
        .filter(User.password_hash == hashlib.sha256(r.get('password').encode()).hexdigest()).first()

    if not u:
        raise Unauthorized('Not allowed to access this site.')

    session['user_id'] = u.id

    return jsonify(UserSchema().dump(u).data)

@user_bp.route('/logout', methods=['POST'])
def logout_user():
    session.pop('user_id')
    return jsonify(deleted=True)