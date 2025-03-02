from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Float, Integer
import os

db = SQLAlchemy()

class ICD10Code(db.Model):
    __tablename__ = "icd10_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    category = Column(String)
    vector = Column(String)  # Store vector as JSON string

    def __repr__(self):
        return f"<ICD10Code {self.code}>"

# Initialize database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()