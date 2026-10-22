from pydantic import BaseModel, ConfigDict, Field, EmailStr

class StudentCreate(BaseModel):
    student_number: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    course: str = Field(min_length=1, max_length=100)
    year_level: int = Field(ge=1, le=6)


class StudentResponse(StudentCreate):
    id: int
    created_at: object

    model_config = ConfigDict(from_attributes=True)