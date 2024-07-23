from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import InternDivision
from app.models.user_profile import UserProfile  # Make sure to import your model properly

class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        load_instance = True


# You can define other schemas here as well
