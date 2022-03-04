from marshmallow import Schema, fields, validates_schema, ValidationError
from cerberus import Validator
from cerberus.errors import BasicErrorHandler


# schema = {'weight': {'min': 10.1, 'max': 10.9}}
# document = {'weight': 12.3}
# v = Validator()
# res = v.validate(document, schema)
# print(res)

schema = {
    "field_a": {
        "type": "integer",
        "min": 3,
        "max": 5,
    },
    "field_b": {
        "type": "integer",
    },
}


class AdamErrorHandler(BasicErrorHandler):
    def __call__(self, errors):
        tree = super(AdamErrorHandler, self).__call__(errors)
        return ["{0}: {1}".format(field, "\n".join(err)) for field, err in tree.items()]


v = Validator(schema, allow_unknown=True, error_handler=AdamErrorHandler)


class NumberSchema(Schema):
    field_a = fields.Integer()
    field_b = fields.Integer()

    @validates_schema(pass_original=True)
    def validate_numbers(self, data, original_data):
        res = v.validate(original_data)
        if not res:
            raise ValidationError(v.errors)


schema = NumberSchema()
result, errors = schema.load({"field_a": 1, "field_b": 2.0, "as": 123})
print(result, errors)
# errors['_schema'] # => ["field_a must be greater than field_b"]
