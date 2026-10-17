# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field

# app = FastAPI()
# class StudentCreate(BaseModel):
#     name : str = Field(min_length=2, max_length=50)
#     age : int = Field(gt=0, lt=150)
# class StudentUpdate(BaseModel):
#     name : str | None = None
#     age : int | None = None
# students = {
#     1: {"id": 1, "name": "Rahul", "age": 21},
#     2: {"id": 2, "name": "Priya", "age": 22},
#     3: {"id": 3, "name": "Amit", "age": 20}
# }
# @app.get("/")
# def home():
#     return {"message": "Welcome to my Student Management Application!"}

# @app.get("/students")
# def get_students():    
#     return list(students.values())

# @app.get("/student/{student_id}")
# def get_studentByid(student_id: int):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return students[student_id]

# @app.put("/student/{student_id}")
# def update_student(student_id: int, student: StudentUpdate):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail="Student not found")
#     student_data = student.dict(exclude_unset=True)
#     students[student_id].update(student_data)
#     return students[student_id]

# next_id = max(students.keys()) + 1
# @app.post("/students")
# def create_student(student : StudentCreate):
#     global next_id
#     new_student = {
#         "id" : next_id,
#         "name" : student.name,
#          "age" : student.age
#     }
    
#     students[next_id] = new_student
#     next_id += 1
#     return new_student


# @app.patch("/student/{student_id}")
# def updateStudent(student_id : int, student: StudentUpdate):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail="Student not found")
#     updates = student.model_dump(exclude_unset=True)
#     students[student_id].update(updates)
#     return students[student_id]

# @app.delete("/student/{student_id}")
# def delete_student(student_id: int):
#     if student_id not in students:
#         raise HTTPException(status_code=404, detail="Student not found")
#     deleted_student = students.pop(student_id)
#     return {"message": "Student deleted successfully", "student": deleted_student}

# using db for the above in below code snippet

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session

# from database import engine, Base, get_db
# from models import Student

# app = FastAPI()

# # Create the database table if it doesn't exist
# Base.metadata.create_all(bind=engine)


# # Request model for creating a student
# class StudentCreate(BaseModel):
#     name: str = Field(min_length=2, max_length=50)
#     age: int = Field(ge=1, le=100)


# # Request model for updating a student
# class StudentUpdate(BaseModel):
#     name: str | None = Field(
#         default=None,
#         min_length=2,
#         max_length=50
#     )
#     age: int | None = Field(
#         default=None,
#         ge=1,
#         le=100
#     )


# @app.get("/")
# def home():
#     return {"message": "Welcome to my Student Management API"}


# # Get all students, with optional filters
# @app.get("/students")
# def get_students(
#     age: int | None = None,
#     name: str | None = None,
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Student)

#     if age is not None:
#         query = query.filter(Student.age == age)

#     if name is not None:
#         query = query.filter(Student.name.ilike(f"%{name}%"))

#     return query.all()


# # Get one student
# @app.get("/students/{student_id}")
# def get_student(
#     student_id: int,
#     db: Session = Depends(get_db)
# ):
#     student = db.query(Student).filter(
#         Student.id == student_id
#     ).first()

#     if student is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Student not found"
#         )

#     return student


# # Create a student
# @app.post("/students", status_code=201)
# def create_student(
#     student: StudentCreate,
#     db: Session = Depends(get_db)
# ):
#     new_student = Student(
#         name=student.name,
#         age=student.age
#     )

#     db.add(new_student)
#     db.commit()
#     db.refresh(new_student)

#     return new_student


# # Update a student
# @app.patch("/students/{student_id}")
# def update_student(
#     student_id: int,
#     student_data: StudentUpdate,
#     db: Session = Depends(get_db)
# ):
#     student = db.query(Student).filter(
#         Student.id == student_id
#     ).first()

#     if student is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Student not found"
#         )

#     updates = student_data.model_dump(exclude_unset=True)

#     for field, value in updates.items():
#         setattr(student, field, value)

#     db.commit()
#     db.refresh(student)

#     return student


# # Delete a student
# @app.delete("/students/{student_id}")
# def delete_student(
#     student_id: int,
#     db: Session = Depends(get_db)
# ):
#     student = db.query(Student).filter(
#         Student.id == student_id
#     ).first()

#     if student is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Student not found"
#         )

#     db.delete(student)
#     db.commit()

#     return {
#         "message": "Student deleted successfully",
#         "student_id": student_id
#     }

# after creating router 
from fastapi import FastAPI

from database import Base, engine
from routers.students import router as students_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(students_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to my Student Management API"
    }