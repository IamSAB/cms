from flask_jwt_extended import current_user, fresh_jwt_required, jwt_required, jwt_optional
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from ..database import db
from .forms import UserForm, RegisterForm, EmailForm, PasswordForm
from .models import User
from ..mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app, redirect, request
from flask_restful import fields, marshal_with

class Email(Resource):

    def get(self):
        data = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='confirm_email').\
            loads(request.args.get('token'))
        user = User.query.get_or_404(data['id'])
        user.email = data['email']
        db.session.commit()
        return {}, 200

    @fresh_jwt_required
    def post(self, id):
        if current_user.id != id:
            current_user.require_permissions([User.Permission.Admin])
        form = EmailForm()
        form.validate_or_422()
        token = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='confirm_email').\
            dumps({
                'id': id,
                'email': form.email.data
            })
        url = f'http://localhost:8080?change_email={token.decode("utf-8")}'
        send_mail(
            'Confirm email change',
            form.email.data,
            f'Hello, please confirm your email by open the following link: {url}'
        )
        return {}, 200

class ChangePassword(Resource):

    @fresh_jwt_required
    def post(self, id):
        form = PasswordForm()
        form.validate_or_422()
        if current_user.id == id:
            current_user.set_password(form.password.data)
        else:
            current_user.require_permissions([User.Permission.Admin])
            user = User.query.get(id)
            user.set_password(form.password.data)
        db.session.commit()
        return {}, 200


class UserResource(Resource):

    @jwt_optional
    def put(self):
        form = RegisterForm()
        form.validate_or_422()
        if current_user:
            current_user.require_permissions([User.Permission.Admin])
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        token = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt='account_activation').dumps({
            'type': 'activate_account',
            'id': user.id
        })
        msg = f'Hello, please confirm your registration: http://localhost:8080?activate={token}'
        send_mail('Registration',form.email.data, msg)
        return form.created()

    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict()

    @jwt_required
    def post(self, id):
        if current_user.id != id:
            current_user.require_permissions([User.Permission.Admin])
        user = User.query.get_or_404(id)
        form = UserForm()
        form.validate_or_422()
        form.populate_obj(user)
        db.session.commit()
        return form.saved()

    @fresh_jwt_required
    def delete(self, id):
        if current_user.id != id:
            current_user.require_permissions([User.Permission.Admin])
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class UsersResource(Resource):

    @jwt_required
    def get(self):
        data =  []
        for user in User.query.all():
            data.append(user.to_dict(['id', 'username', 'email', 'forename', 'surname']))
        return { 'users': data }

    @fresh_jwt_required
    def post(self):
        data = request.get_json()
        users = User.query.\
            filter(User.id.in_(data['ids'])).\
            all()
        for user in users:
            user.status = User.Status.Activated
        db.session.commit()
        return {'msg': f'Updated {users.length} users.'}, 200


    @fresh_jwt_required
    def delete(self):
        data = request.get_json()
        users = User.query.\
            filter(User.id.in_(data['ids'])).\
            all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return {}, 204
