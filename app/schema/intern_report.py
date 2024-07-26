
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.intern_finished import InternFinished
from marshmallow import fields
class InternReportSchema(SQLAlchemyAutoSchema):
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    intern_certification = fields.Str()
    division_name = fields.Str()
    fullname = fields.Str()