
# Student Management API

A REST API built using Python, FastAPI, SQLAlchemy, and SQLite to manage student records.

## Features

- Create a student
- View all students
- Search students by name or age
- View a student by ID
- Update student details
- Delete a student
- Validate request data
- Store records in an SQLite database

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Installation

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:

   ```bash
   fastapi dev main.py
   ```

5. Open the API documentation:

   http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/students` | Get all students |
| GET | `/students/{student_id}` | Get one student |
| POST | `/students` | Create a student |
| PATCH | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
