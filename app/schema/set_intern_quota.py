from marshmallow import Schema, fields, validate, ValidationError, post_load

class SetInternQuota(Schema):
    division_id = fields.Int(required=True)
    duration = fields.Str(required=True)
    quota = fields.Int(required=True, validate=validate.Range(min=0))
