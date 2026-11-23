from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "민수", "score": 90},
    {"id": 2, "name": "지수", "score": 85},
    {"id": 3, "name": "현우", "score": 100}
]
class StudentCreate(BaseModel):
    name:str
    score: int

@app.post("/students",status_code=201)
def create_student(student:StudentCreate):
    new_student = {
        "id" = len(students)+1,
        "name" = student.name,
        "score" = student.score
    }
    students.append(new_student)

    return new_student

@app.get("/students/{student_id}")
def get_student(student_id:int):
    for student in students:
        if (student["id"]) == student_id:
            return student

    raise HTTPException(
        status_code= 404
        detail="느가 찾는 학생 읎다"
    )
 