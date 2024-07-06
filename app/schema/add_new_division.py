from marshmallow import Schema, fields, validate, ValidationError, post_load

class AddNewDivision(Schema):
    division_name = fields.Str(required=True, validate=validate.Length(min=6))
