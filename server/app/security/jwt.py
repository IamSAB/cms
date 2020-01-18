import json
from datetime import datetime, timedelta

import jwt


def generate(username):
    iat = datetime.utcnow()
    exp = iat + timedelta(seconds=current_app.config.get('JWT_EXPIRATION'))
    nbf = iat + timedelta(seconds=current_app.config.get('JWT_NOT_BEFORE'))
    payload = {'iat': iat, 'exp': exp, 'nbf': nbf, 'username': username}
    return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256').decode('utf-8')


def validate(token):
    try:
        return jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithm='HS256')
    except jwt.ExpiredSignatureError:
        raise Unauthorized('Signature has expired.')
    except jwt.DecodeError:
        raise Unauthorized('Error decoding signature.')
    except jwt.InvalidTokenError:
        raise Unauthorized('Invalid token.')
