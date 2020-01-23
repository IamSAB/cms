from flask_jwt_extended import current_user, fresh_jwt_required, jwt_required
from flask_restful import Resource

from ..database import db
from .forms import AccountForm, RegisterForm
from .models import User


class MeResource(Resource):

    @jwt_required
    def get(self):
        return current_user.to_dict(['username', 'email', 'forename', 'surname'])

    @fresh_jwt_required
    def post(self):
        form = AccountForm()
        if form.validate_on_submit():
            form.populate_obj(current_user)
            db.session.commit()
            return form.get_data(), 200
        return form.get_errors(), 400

    @fresh_jwt_required
    def delete(self):
        db.session.delete(current_user)
        return {}, 204


class UserResource(Resource):

    @fresh_jwt_required
    def put(self):
        form = RegisterForm()
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            return form.get_data(), 201
        return form.get_errors(), 400

    def get(self, id):
        return User.query.get(id).to_dict(['username', 'email', 'forename', 'surname'])

    @jwt_required
    def post(self, id):
        user = User.query.get_or_404(id)
        form = AccountForm()
        if form.validate_on_submit():
            form.populate_obj(user)
            db.session.commit()
            return form.get_data(), 200
        return form.get_errors()

    @fresh_jwt_required
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        return {}, 204

class UsersResource(Resource):

    @jwt_required
    def get(self):
        data =  []
        for user in User.query.all():
            data.append(user.to_dict(['username', 'email', 'forename', 'surname']))
        return { 'users': data }
