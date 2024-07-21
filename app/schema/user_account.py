from marshmallow import Schema, fields, validate, ValidationError, post_load
import bcrypt
from app.models import UserAccount

class UserAccountSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=6))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    