from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student
from schemas import StudentCreate, StudentResponse

app = FastAPI(title="Student Management API")

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()

@app.post("/students"
        response_model=StudentResponse,
        status_code=status.HTTP_201_CREATED
)
def create_student(
    student: studentCreate,
    db: Session = Depends(get_db)
);

    existing = db.query(Student).filter(
        (Student.student_number == student.student_number) | (Student.email == student.email)
    ).

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Student number or email already exists"
        )

    new_student = student ()