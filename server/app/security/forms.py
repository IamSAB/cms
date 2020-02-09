from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from ..form import JsonForm
from ..user.models import User

class LoginForm(JsonForm):

    identity = StringField('Identity', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    user = None
    validation_exception_description = 'Incorrect username or password.'

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        self.user = User.get_by_login(self.identity.data)
        if self.user is None or not self.user.validate_password(self.password.data):
            return False
        return True
