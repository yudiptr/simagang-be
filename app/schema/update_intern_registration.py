from marshmallow import Schema, fields

class UpdateInternRegistration(Schema):
    registration_ids = fields.List(fields.Integer, required=True)
