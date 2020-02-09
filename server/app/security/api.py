import json
from functools import wraps

from flask import Blueprint, _request_ctx_stack, current_app, jsonify, request
from werkzeug.exceptions import Unauthorized, Forbidden, BadRequest
from werkzeug.local import LocalProxy

from ..user.models import User
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, fresh_jwt_required, current_user
)
from .forms import LoginForm
from ..user.forms import PasswordForm
from ..mail import send_mail

jwt = JWTManager()

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'id': user.id}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.filter(User.username == identity).first()

def permissions(perms):
    def f(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user:
                raise Unauthorized('No current user')
            if not current_user.has_permissions(perms):
                raise Forbidden('Not required permssions')
            fn(*args, **kwargs)
        return wrapper
    return f


class Activation(Resource):

    def post(self):
        data = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='activate_account').\
            loads(request.get_json()['token'])
        user = User.query.get_or_404(data.id)
        user.account_activation = True
        db.session.commit()
        return {}, 200


class ForgotPassword(Resource):

    def get(self):
        json = request.get_json()
        user = User.query.get_by_login(json['identity'])
        token = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='forgot_password').\
            dumps({'id': user.id })
        url = url_for('/', reset_password=token, _external=True)
        send_mail('Reset password', user.email, f'Hello, please reset your password by open the following link: {url}')
        return {}, 200

    def post(self):
        form = PasswordForm()
        form.validate_or_422()
        json = request.get_json()
        data = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='forgot_password').\
            loads(json['token'])
        user = User.query.get(data['id'])
        user.set_password(form.password.data)
        db.session.commit()
        return {}, 200


class Login(Resource):

    def post(self):
        form = LoginForm()
        form.validate_or_422()
        return {
            'access_token': create_access_token(identity=form.user, fresh=True),
            'refresh_token': create_refresh_token(identity=form.user)
        }


class Refresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        return {'access_token': create_access_token(identity=current_user, fresh=False)}


class FreshLogin(Resource):

    def post(self):
        form = LoginForm()
        form.validate_or_422()
        return {
            'access_token': create_access_token(identity=form.user, fresh=True)
        }
