from marshmallow import Schema, fields, validate, ValidationError, post_load
from app.choices.gender import Genders
from app.models.user_profile import UserProfile

class UserProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    fullname = fields.Str(required=True, validate=validate.Length(min=1))
    student_number = fields.Str(required=True, validate=validate.Regexp('^[0-9]+$', error="Student number must be numeric."))
    ipk = fields.Decimal(required=True, as_string=False, validate=validate.Range(min=0, max=4))
    phone_number = fields.Str(required=True, validate=validate.Regexp(r'^\+?[0-9]+$', error="Phone number must be numeric and can start with +."))
    university = fields.Str(required=True, validate=validate.Length(min=1))
    semester = fields.Int(required=True, validate=validate.Range(min=1, max=12))
    gender = fields.Str(required=True, validate=validate.OneOf([gender.value for gender in Genders]))
    email = fields.Str(required=True)
    
    @post_load
    def make_user(self, data, **kwargs):
        return UserProfile(**data)