from flask import Blueprint, jsonify, request

from ..database import db
from flask_jwt_extended import jwt_required
from .models import User

user = Blueprint('user', __name__, url_prefix='/api/user')


@user.route('/me', methods=['POST'])
@jwt_required
def me():
    return jsonify(current_user.to_dict(['username','email','forename','surname']))


@user.route('/register', methods=['POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return form.jsonify(), 200

    return form.jsonify(), 422
