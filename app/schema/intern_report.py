
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.intern_finished import InternFinished

class InternReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InternFinished
        load_instance = True
