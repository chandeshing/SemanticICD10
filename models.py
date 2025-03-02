from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Float, Integer
import os

db = SQLAlchemy()

class MedicalCode(db.Model):
    __tablename__ = "medical_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    classifier_type = Column(String)  # New field for classifier type
    vector = Column(String)  # Store vector as JSON string

    def __repr__(self):
        return f"<MedicalCode {self.classifier_type}:{self.code}>"

# Initialize database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()