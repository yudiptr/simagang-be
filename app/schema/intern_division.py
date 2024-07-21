from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models import InternDivision  # Make sure to import your model properly

class InternDivisionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InternDivision
        load_instance = True

    id = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    division_name = auto_field()

# You can define other schemas here as well
