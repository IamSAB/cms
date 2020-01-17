from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .api.auth import auth, set_jwt_header
from .api.user import user
from .models import User, db

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

# load config
app.config.from_object('config')  # load ./config.py
app.config.from_pyfile('config.py')  # load ./instance/config.py

db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(auth)
app.register_blueprint(user)

@app.after_request
def after_request_func(response):
    return set_jwt_header(response)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }, e.code

@app.route('/')
def home ():
    return 'Hello World'
