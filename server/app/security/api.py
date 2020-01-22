
import json
from functools import wraps

from flask import Blueprint, _request_ctx_stack, current_app, jsonify, request
from werkzeug.exceptions import Unauthorized
from werkzeug.local import LocalProxy

from ..user.models import User
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, fresh_jwt_required
)
from .forms import LoginForm

jwt = JWTManager()

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'username': user.username}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.filter(User.username == identity).first()


class Login(Resource):

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            data = form.get_data()
            user = User.query.\
                filter((User.username == data['username']) | (User.email == data['username'])).\
                first()
            if user and user.validate_password(data['password']):
                return {
                    'access_token': create_access_token(identity=user, fresh=True),
                    'refresh_token': create_refresh_token(identity=user)
                }
            else:
                raise Unauthorized('Username or password incorrect.')

        return form.get_errors(), 400


class Refresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        return {'access_token': create_access_token(identity=get_jwt_identity(), fresh=False)}


class FreshLogin(Resource):

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            data = form.get_data()
            user = User.query.\
                filter((User.username == data['username']) | (User.email == data['username'])).\
                first()
            if user and user.validate_password(data['password']):
                return {'access_token': create_access_token(identity=user, fresh=True)}
            else:
                raise Unauthorized('Username or passsword incorrect.')
        return form.get_errors(), 400
