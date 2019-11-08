import base64
import hashlib
import os
from functools import wraps

from flask import session, request, jsonify, redirect, url_for, g, Flask


SALT_LENGTH = 16


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    from login.views import login_view
    app.register_blueprint(login_view)

    from api.views import api_view
    app.register_blueprint(api_view)

    from database import db
    db.init_app(app)

    return app


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_LENGTH)
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return base64.encodebytes(salt+key).decode('utf-8')


def check_password(password: str, user_hash: str):
    raw_hash = base64.decodebytes(user_hash.encode('utf-8'))
    user_salt = raw_hash[:SALT_LENGTH]
    user_key = raw_hash[SALT_LENGTH:]
    key = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), user_salt, 100000,
    )
    return key == user_key


def is_user_in_session() -> bool:
    return 'user_id' in session and session.get('user_id') is not None


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_user_in_session():
            if 'X-API-Request' in request.headers:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('login_view.login'))
        return func(*args, **kwargs)
    return wrapper


def permission_required(role_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_user_in_session() and g.user.role.name != role_name:
                return 'Access denied', 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
