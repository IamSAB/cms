from flask import Flask
from .api.user import user
from .api.auth import auth
from .database import db

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(auth)

@app.route('/')
def hello_world():
    return 'This is a simple API server!'
