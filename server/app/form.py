from flask import jsonify, request
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm


class JsonForm(FlaskForm):

    def get_errors(self):
        errors = {}
        for name, msgs in self.errors.items():
            errors[name] = []
            for msg in msgs:
                errors[name].append(msg)
        return errors

    def get_data(self):
        data = {}
        for name, field in self._fields.items():
            data[name] = field.data
        return data

    def jsonify(self):
        return jsonify({
            'data': self.get_data(),
            'errors': self.get_errors()
        })
