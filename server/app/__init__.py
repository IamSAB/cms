import time

from flask import Flask, jsonify
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException

from .async_api import TaskStatus, async_api, async_api_cleaning
from .database import db
from .mail import mail, send_mail
from .security.api import FreshLogin, Login, Refresh, jwt
from .user.api import user

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

# load config
app.config.from_object('config')  # load ./config.py
app.config.from_pyfile('config.py')  # load ./instance/config.py

db.init_app(app)
mail.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user)


@app.before_first_request
def before_first_request():
    async_api_cleaning()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    }), e.code

# setup API
api = Api(app, prefix='/api')

# security resources
api.add_resource(Login, '/security/login')
api.add_resource(Refresh, '/security/refresh')
api.add_resource(FreshLogin, '/security/freshlogin')

# async resources
api.add_resource(TaskStatus, '/task/<task_id>')
