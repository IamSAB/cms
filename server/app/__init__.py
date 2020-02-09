import time

from flask import Flask, jsonify
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

from .async_api import TaskStatus, async_api, async_api_cleaning
from .database import db
from .form import ValidationException
from .mail import mail, send_mail
from .security.api import (Activation, ForgotPassword, FreshLogin, Login,
                           Refresh, jwt)
from .user.api import ChangePassword, Email, UserResource, UsersResource

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

# load config
app.config.from_object('config')  # load ./config.py
app.config.from_pyfile('config.py')  # load ./instance/config.py

db.init_app(app)
mail.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

@app.before_first_request
def before_first_request():
    async_api_cleaning()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        'msg': e.description,
    }), e.code


class CmsApi(Api):

    def handle_error(self, e):
        data = {
            'msg': e.description
        }
        if isinstance(e, ValidationException):
            data['errors'] = e.errors
        return jsonify(data), e.code

@app.route('/')
def index ():
    return 'API'

# setup API
api = CmsApi(app, prefix='/api')

# security resources
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Refresh, '/refresh', endpoint='refreshlogin')
api.add_resource(FreshLogin, '/freshlogin', endpoint='freshlogin')
api.add_resource(ForgotPassword, '/password', endpoint='forgot_password')
api.add_resource(Activation, '/activate', endpoint='activate')

# user resources
api.add_resource(ChangePassword, '/user/<int:id>/password', endpoint='user_password')
api.add_resource(Email, '/user/<int:id>/email', '/email', endpoint='user_email')
api.add_resource(UserResource, '/user/<int:id>', '/user', endpoint='user')
api.add_resource(UsersResource, '/users', endpoint='users')

# async resources
api.add_resource(TaskStatus, '/task/<string:task_id>')
