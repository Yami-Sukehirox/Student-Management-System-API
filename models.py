from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from database import Base


class student(Base):
    _tablename_ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(string(20), unique=True, nullable=False)
    first_name = Column(string(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    course = Column(String(100), nullable=False)
    year_level Column(Integer, nullable=False)
    created_at = Column(TIMESTAP, server_default=text("CURRENT_TIMESTAMP"))