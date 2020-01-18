
import json
from functools import wraps

from flask import Blueprint, _request_ctx_stack, current_app, jsonify, request
from werkzeug.exceptions import Unauthorized
from werkzeug.local import LocalProxy

from ..user.models import User
from . import jwt

security = Blueprint('security', __name__, url_prefix='/api/security')

current_user = LocalProxy(lambda: getattr(
    _request_ctx_stack.top, 'current_user', None))

def append_jwt(response):
    if (current_user):
        data = json.loads(response.get_data())
        data['jwt'] = jwt.generate(current_user.username)
        response.set_data(json.dumps(data))
    return response

def authenticated(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return Unauthorized()
        payload = jwt.validate(token)
        user = User.query.\
            filter(User.username == payload['username']).\
            first()
        if not user:
            raise Unauthorized()
        _request_ctx_stack.top.current_user = user
        return fn(*args, **kwargs)
    return decorator


@security.route('/authenticate', methods=['POST'])
def authenticate():
    json = request.get_json()

    user = User.query.\
        filter((User.username == json['username']) | (User.email == json['username'])).\
        first()

    if user and user.validate_password(json['password']):
        return jsonify({'jwt': jwt.generate(user.username)})
    else:
        return Unauthorized()


@security.route('/authorize', methods=['POST'])
@authenticated
def authorize():
    return jsonify({
        permissions: current_user.permissions
    })
