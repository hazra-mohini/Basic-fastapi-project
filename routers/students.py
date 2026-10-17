from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student
from schemas import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("")
def get_students(
    age: int | None = None,
    name: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    if age is not None:
        query = query.filter(Student.age == age)

    if name is not None:
        query = query.filter(Student.name.ilike(f"%{name}%"))

    return query.all()


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post("", status_code=201)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    student = Student(
        name=student_data.name,
        age=student_data.age
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


@router.patch("/{student_id}")
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    updates = student_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    for field, value in updates.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }