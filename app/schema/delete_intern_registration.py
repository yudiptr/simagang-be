from marshmallow import Schema, fields

class DeleteInternRegistration(Schema):
    registration_id = fields.Int(required=True)
