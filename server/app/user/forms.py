from flask import url_for
from wtforms import ValidationError
from wtforms.fields import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo

from ..form import JsonForm
from .models import User


class UserForm(JsonForm):

    username = StringField(validators=[DataRequired()])
    forename = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])

    def validate_username(self, field):
        user = User.query.\
            filter(User.username == field.data).\
            first()
        if user and user.username != field.data:
            raise ValidationError('Username already registered.')

class PasswordForm(JsonForm):

    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])

    def populate_obj(self, user: User):
        super().populate_obj(user)
        user.set_password(self.password.data)

class EmailForm(JsonForm):

    email = EmailField()

    def validate_email(self, field):
        user = User.query.\
            filter(User.email == field.data).\
            first()
        if user is not None:
            raise ValidationError('Email already registered.')

class RegisterForm(PasswordForm, EmailForm, UserForm):
    pass
