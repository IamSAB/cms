from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .database import db
from .security.api import security, append_jwt
from .user.api import user

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

# load config
app.config.from_object('config')  # load ./config.py
app.config.from_pyfile('config.py')  # load ./instance/config.py

db.init_app(app)

with app.app_context():
    db.create_all()

# register blueprint
app.register_blueprint(security)
app.register_blueprint(user)


@app.after_request
def after_request_func(response):
    return append_jwt(response)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    }), e.code


@app.route('/')
def home():
    return jsonify(msg='I am online ;P')
