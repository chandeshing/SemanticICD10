from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    category = Column(String)
    vector = Column(String)  # Store vector as JSON string

    def __repr__(self):
        return f"<ICD10Code {self.code}>"

# Create tables
Base.metadata.create_all(bind=engine)
