from flask_sqlalchemy import Model, SQLAlchemy

from .utils import auto_repr


class ExtendedModel(Model):

    def to_dict(self, properties=None):
        if not properties:
            return dict((column.name, getattr(self, column.name)) for column in self.__table__.columns)
        else:
            data = {}
            for column in self.__table__.columns:
                if column.name in properties:
                    data[column.name] = getattr(self, column.name)
            return data

    def __repr__(self):
        return auto_repr(self, [column.name for column in self.__table__.columns])

    def __str__(self):
        return repr(self)


db = SQLAlchemy(model_class=ExtendedModel)
