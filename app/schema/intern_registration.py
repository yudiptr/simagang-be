
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models.intern_division import InternDivision
from app.models.intern_registration import InternRegistration

class InternRegistrationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InternRegistration
        load_instance = True
