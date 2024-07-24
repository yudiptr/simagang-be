
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.choices.intern_registration_status import InternRegistrationStatus
from app.models.intern_division import InternDivision
from app.models.intern_registration import InternRegistration
from marshmallow import fields, Schema
class InternRegistrationSchema(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    status = fields.Enum(InternRegistrationStatus, by_value=True)
    cv = fields.Str()
    cover_letter = fields.Str()
    student_card = fields.Str()
    photo = fields.Str()
    proposal = fields.Str()
    duration = fields.Str()
    division_id = fields.Int()
    division_name = fields.Str()
    fullname = fields.Str()