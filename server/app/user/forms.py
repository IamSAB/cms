from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo

from ..form import JsonForm


class RegisterForm(JsonForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired(), EqualTo(
        'confirm', message='Passwords must match')])
    username = StringField(validators=[DataRequired()])
    forename = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])
