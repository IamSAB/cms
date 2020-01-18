import hashlib

from ..database import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    forename = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)

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
