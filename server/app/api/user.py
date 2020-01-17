from flask import Blueprint, jsonify, request
from .auth import current_user, jwt_required
from ..models import User, db

user = Blueprint('user', __name__, url_prefix='/api/user')

@user.route('/me', methods=['POST'])
@jwt_required
def me():
    u = current_user
    return jsonify(
        username=u.username,
        forename=u.forename,
        surname=u.surname,
        email=u.email
    )

@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user = User(
        username=data['username'],
        forename=data['forename'],
        surname=data['surname'],
        email=data['email']
    )

    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'msg': 'Success'
    })
