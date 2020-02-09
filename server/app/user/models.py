import hashlib
import os
from werkzeug.exceptions import Forbidden
from ..database import db


class User(db.Model):

    class Status():
        Deactivated = 1
        Activated = 2
        Blocked = 3

    class Permission():
        Admin = 1
        Manager = 2

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    forename = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    confirmed_email = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, default=Status.Deactivated)
    permissions = db.Column(db.Integer, default=0)

    def require_permissions(self, permission_set):
        permissions = sum(permission_set)
        if not permission & self.permissions == permissions:
            raise Forbidden('Unsufficient user rights.')

    def hash_password(self, password):
        if not self.salt:
            self.salt = os.urandom(8).hex()
        hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('UTF-8'),
            self.salt.encode('UTF-8'),
            1000
        )
        return hash.hex()

    def set_password(self, password):
        self.password = self.hash_password(password)

    def validate_password(self, password):
        return self.hash_password(password) == self.password

    @classmethod
    def get_by_login(self, identity):
        return self.query.\
            filter((self.username == identity) | (self.email == identity)).\
            first_or_404('Unknown identity.')
