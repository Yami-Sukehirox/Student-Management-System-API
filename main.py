from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student
from schemas import StudentCreate, StudentResponse, StudentUpdate

app = FastAPI(title="Student Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Student).filter(
        (Student.student_number == student.student_number)
        | (Student.email == student.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Student number or email already exists"
        )

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.id).all()

    return students

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing = db.query(Student).filter(
        ((Student.student_number == student_data.student_number)
         | (Student.email == student_data.email))
        & (Student.id != student_id)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Student number or email already exists"
        )

    student.student_number = student_data.student_number
    student.first_name = student_data.first_name
    student.last_name = student_data.last_name
    student.email = student_data.email
    student.course = student_data.course
    student.year_level = student_data.year_level

    db.commit()
    db.refresh(student)

    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return None
