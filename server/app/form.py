from flask import jsonify, request
from werkzeug.datastructures import MultiDict
from wtforms import Form

# https://github.com/underdogio/flask-json-multidict/
def get_json_multidict(request):
    """Extract MultiDict from `request.get_json` to produce similar MultiDict to `request.form`"""
    # Extract our JSON
    body = request.get_json()

    # Iterate over the values
    multi_dict_items = []
    for key in body:
        # If the item is a list (e.g. `['hello', 'world']`, iterate its values
        value = body[key]
        if isinstance(value, list):
            for subvalue in value:
                # If the subvalue is a primitive, save it (e.g. `key -> 'hello'`)
                # DEV: We ignore non-primitives for consistency with what `application/x-www-form-urlencoded` accepts
                if not isinstance(subvalue, list) and not isinstance(subvalue, dict):
                    multi_dict_items.append((key, subvalue))
        # If we have a dictionary, ignore it
        # DEV: We ignore non-primitives for consistency with what `application/x-www-form-urlencoded` accepts
        elif isinstance(value, dict):
            pass
        # Otherwise, save the key/value pair
        else:
            multi_dict_items.append((key, value))

    # Return our generated multidict
    return MultiDict(multi_dict_items)


class JsonForm(Form):

    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        formdata = {**get_json_multidict(request), **formdata}
        super(Form, self).__init__(formdata=formdata, obj=obj,
                                   prefix=prefix, data=data, meta=meta, **kwargs)

    def jsonify(self):

        data = {}
        errors = {}

        for name, msgs in self.errors.items():
            errors[name] = []
            for msg in msgs:
                errors[name].append(msg)

        for name, field in iteritems(self._fields):
            data[name] = field.data

        return jsonify({
            'data': data,
            'errors': errors
        })
