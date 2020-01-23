from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo

from ..form import JsonForm


class AccountForm(JsonForm):
    username = StringField(validators=[DataRequired()])
    forename = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])


class RegisterForm(AccountForm):
    email = StringField(validators=[Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired(), EqualTo(
        'confirm', message='Passwords must match')])
