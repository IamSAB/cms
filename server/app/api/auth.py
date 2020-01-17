import json
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Blueprint, _request_ctx_stack, current_app, jsonify, request
from werkzeug.exceptions import Unauthorized
from werkzeug.local import LocalProxy

from ..models import User

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

current_user = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_user', None))

def generate_jwt(username):
    iat = datetime.utcnow()
    exp = iat + timedelta(seconds=current_app.config.get('JWT_EXPIRATION'))
    nbf = iat + timedelta(seconds=current_app.config.get('JWT_NOT_BEFORE'))
    payload = {'iat': iat, 'exp': exp, 'nbf': nbf, 'username': username}
    return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256').decode('utf-8')

def validate_jwt(token):
    try:
        return jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithm='HS256')
    except jwt.ExpiredSignatureError:
        raise Unauthorized('Signature has expired.')
    except jwt.DecodeError:
        raise Unauthorized('Error decoding signature.')
    except jwt.InvalidTokenError:
        raise Unauthorized('Invalid token.')

def jwt_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return Unauthorized()
        payload = validate_jwt(token)
        user = User.query.\
            filter(User.username==payload['username']).\
            first()
        if not user:
            raise Unauthorized()
        _request_ctx_stack.top.current_user = user
        return fn(*args, **kwargs)
    return decorator

def set_jwt_header(response):
    if (current_user):
        data = json.loads(response.get_data())
        data['jwt'] = generate_jwt(current_user.username)
        response.set_data(json.dumps(data))
    return response

@auth.route('/jwt', methods=['POST'])
def authenticate():
    json = request.get_json()

    user = User.query.\
        filter( (User.username == json['username']) | (User.email == json['username'])).\
        first()

    if user and user.validate_password(json['password']):
        return jsonify({'jwt': generate_jwt(user.username)})
    else:
        return Unauthorized()
