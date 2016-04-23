from flask import session, g
from werkzeug.exceptions import Unauthorized
from functools import wraps

from api.models import db_session, User

def requires_authentication(role=None):
    def auth_decorator(func):
        @wraps(func)
        def func_wrapper():
            if 'user_id' in session:
                u = User.query.get(session['user_id'])
                if u is not None:
                    g.user_id = u.id
                    g.user_role = u.role

                    if not role or (role and u.role == role):
                        return func()

                raise Unauthorized()

        return func_wrapper
    return auth_decorator