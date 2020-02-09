from flask import jsonify, request
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from werkzeug.exceptions import HTTPException

class ValidationException(HTTPException):

    code = 422
    name = 'Failed Validation'
    description = 'Your submission raised a validation error.'
    errors = []

    def __init__(self, description=None, errors=[], response=None):
        super().__init__(description, response)
        self.errors = errors

class JsonForm(FlaskForm):

    validation_exception_description = ''

    def validate_or_422(self):
        if not self.validate_on_submit():
            if self.validation_exception_description:
                raise ValidationException(self.validation_exception_description, self.get_errors())
            else:
                raise ValidationException(errors=self.get_errors())

    def created(self):
        return self.get_data(), 201

    def saved(self):
        return self.get_data(), 200

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
