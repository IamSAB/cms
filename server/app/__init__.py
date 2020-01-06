from flask import Flask
from flask_jwt import JWT
from .models import db, User

app = Flask(__name__, instance_relative_config=True, static_url_path='/static')

# load config
app.config.from_object('config')  # load ./config.py
app.config.from_pyfile('config.py')  # load ./instance/config.py

# initizalize database
from .models import db
db.init_app(app)

with app.app_context():
    db.create_all()

# flask-jwt implementation
def identity(payload):
    return User.query.filter(User.id == payload['identity']).scalar()

def authenticate(username, password):
    user = User.query.\
        filter( (User.username == username) | (User.email == username)).\
        first()

    if user and user.validate_password(password):
        return user

jwt = JWT(app, authenticate, identity)

# register blueprints
from .api.user import user

app.register_blueprint(user)

# views
@app.route('/')
def hello_world():
    return 'This is a simple API server!'
