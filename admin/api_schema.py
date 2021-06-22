from marshmallow import Schema, fields, validate


class FooSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    age = fields.Integer(validate=validate.Range(min=18, max=60))


class CreateFooSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    age = fields.Integer(validate=validate.Range(min=18, max=60))
