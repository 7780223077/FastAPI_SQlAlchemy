from sqlalchemy import Column, String, Integer
from database import Base

class Employee(Base):
    __tablename__ = 'Employee'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), index=True)  # Specify length for VARCHAR
    last_name = Column(String(255), index=True)   # Specify length for VARCHAR
    gender = Column(String(50), index=True)       # Specify length for VARCHAR
    age = Column(Integer)
