import hashlib
import os

from flask_sqlalchemy import Model, SQLAlchemy

from .utils import auto_repr


class BaseModel(Model):

    def to_dict(model):
        return dict((column.name, getattr(model, column.name)) for column in model.__table__.columns)

    def __repr__(self):
        return auto_repr(self, ['id'])

    def __str__(self):
        return repr(self)


db = SQLAlchemy(model_class=BaseModel)
