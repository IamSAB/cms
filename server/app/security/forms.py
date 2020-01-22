from wtforms import StringField, PasswordField
from ..form import JsonForm

class LoginForm(JsonForm):
    username =  StringField()
    password = PasswordField()
