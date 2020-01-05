from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/')
def hello_world():
    return 'Endpoint auth API'
