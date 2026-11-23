from fastapi import FastAPI , HTTPException
from pydantic import BaseModel #클라이언트가 보낸 데이터 검증.
#웹 요청을 처리할 프로그램을 준비하는 것
app = FastAPI()

students = [
    {"id": 1, "name": "민수", "score": 90},
    {"id": 2, "name": "지수", "score": 85},
    {"id": 3, "name": "현우", "score": 100}
]

#클라이언트가 보내야할 데이터의 구조를 정의
#BaseModel: Pydantic 라이브러리가 제공하는 클래스로, 데이터 검증 기능을 갖음.
class StudentCreate(BaseModel):
    name: str
    score: int

#get → HTTP의 GET 요청을 처리
#"/" → 요청할 URL 경로
#해당 경로로 GET 요청이 들어오면 아래 함수를 실행하도록 등록

#FastAPI는 요청받은 URL 경로에 따라 서로 다른 Python 함수를 실행
#수정했으면 저장해야 서버가 자동으로 다시 실행.
# @app.get("/")
# def home():
#     return {"message":"hello backend!"}

# @app.get("/hello")
# def hello():
#    return {"message":"안녕하세요!"}

# @app.get("/score")
# def get_score():
#     return {"name": "민수", "score": 100}

@app.get("/students")
def get_students(min_score: int =0,max_score: int = 100): #0은 값을 전달하지 않았을 때 기본값.
    result = [] #조건에 맞는 학생들을 저장할 리스트.

    for student in students:
        if max_score >= student["score"] >= min_score:
            result.append(student)

    return {"students":result} #최종 결과를 json으로 반환.

#딕셔너리를 사용하는 이유는 데이터에 이름을 붙여 전달하기 편해서. 반드시 딕셔너리일
#필요는 없다.
@app.get("/students/{student_id}")
def get_student(student_id:int): # :int는 학생 id가 정수여야 한다는 의미.
    #파이선에서는 자료형 나타내는 방식이 저거니까 외워라
    for student in students:
        if student["id"] == student_id:
            return student #정상적인 결과 반환.

    raise HTTPException( #http 오류를 발생시키는 예외 클래스
        status_code=  404, #응답 상태 코드를 404로 설정
        detail="학생을 찾을 수 없습니다" #오류에 대한 설명.
    )

@app.post("/students",status_code=201) #정상적으로 학생 생성하면,201반환.
#클라이언트가 보낸 json 데이터를 studentcreate 모델에 맞게 검증하고 python 객체로 만듦
def create_student(student: StudentCreate):
    new_student = {
        "id": len(students)+1,
        "name": student.name,
        "score": student.score
    }
    students.append(new_student)

    return new_student