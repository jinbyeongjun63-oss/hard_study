from fastapi import FastAPI , HTTPException
from pydantic import BaseModel,Field  #클라이언트가 보낸 데이터 검증.
#Field는 변수에 추가적인 데이터 검증 조건을 설정할 수 있게 해주는 기능.
import mysql.connector
import os
# 터미널에 작성하는 환경변수 변수
# $env:MYSQL_PASSWORD = Read-Host -MaskInput "MySQL password"
# 환경변수란? 운영체제의 실행 환경에 값을 저장해두고 프로그램에서 가져다 쓸 수      있도록  하는 변수.
#웹 요청을 처리할 프로그램을 준비하는 것
app = FastAPI()

def get_connection():
    conn = mysql.connector.connect( #mysql과 연결
        host="localhost", # 내 컴터 mysql서버
        user="root", #mysql 접속 비밀번호
        password=os.environ["MYSQL_PASSWORD"], #mysql접속 비번
        database="backend_study" #사용할 데이터베이스
    )

    return conn # 생성한 데이터베이스 연결 객체 반환


students = [
    {"id": 1, "name": "민수", "score": 90},
    {"id": 2, "name": "지수", "score": 85},
    {"id": 3, "name": "현우", "score": 100}
]

#클라이언트가 보내야할 데이터의 구조를 정의
#BaseModel: Pydantic 라이브러리가 제공하는 클래스로, 데이터 검증 기능을 갖음.
class StudentCreate(BaseModel):
    name: str = Field(min_length=1,max_length=20)
    score: int = Field(ge=0,le=100) # 0이상, 100 이하

# ctrl+shit+k: 한줄 다 지우기
class StudentUpdate(BaseModel):
    #이름이나 점수를 입력하지 않아도 오류가 발생하지 않음 
    name: str | None = Field(default=None, min_length=1,max_length=20)   #  |None    :None도 받을 수 있음
    score: int | None = Field(default=None,ge=0,le=100)  #  =None    :값을 전달하지 않으면 기본값은 None
    #ge= greater than or Equal// le = less than or equal

# response_model: 서버->클라이언트에게 반환.
# response모델은 클래스에 정의된 내용만 반환. 다른 정보가 들어있어도 안보냄.
class StudentResponse(BaseModel):
    id: int
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


# sql연결 전 get########################################################
# @app.get("/students")
# def get_students(min_score: int =0,max_score: int = 100): #0은 값을 전달하지 않았을 때 기본값.
#     result = [] #조건에 맞는 학생들을 저장할 리스트.

#     for student in students:
#         if max_score >= student["score"] >= min_score:
#             result.append(student)

#     return {"students":result} #최종 결과를 json으로 반환.

#딕셔너리를 사용하는 이유는 데이터에 이름을 붙여 전달하기 편해서. 반드시 딕셔너리일
#필요는 없다.
# @app.get("/students/{student_id}")
# def get_student(student_id:int): # :int는 학생 id가 정수여야 한다는 의미.
#     #파이선에서는 자료형 나타내는 방식이 저거니까 외워라
#     for student in students:
#         if student["id"] == student_id:
#             return student #정상적인 결과 반환.

#     raise HTTPException( #http 오류를 발생시키는 예외 클래스
#         status_code=  404, #응답 상태 코드를 404로 설정
#         detail="학생을 찾을 수 없습니다" #오류에 대한 설명.
#     )


# sql연결 후 get함수##################################################
@app.get("/students")
def get_students():
    conn = get_connection() #mysql 연결
    cursor = conn.cursor(dictionary=True) #sql명령을 실행할 객체 생성
    # dctionary=True 딕셔너리 형태로 가져와라., false->value만 가져옴
    # 딕셔너리 형태로 가져오면 컬럼이 붙어서 json응답을 만들기 편해짐.
    cursor.execute("SELECT * FROM students") #명령 실행
    result = cursor.fetchall() #모든 행 가져오기

    cursor.close()
    conn.close() 

    return {"students":result}

@app.get("/students/{student_id}")
def get_students(student_id:int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "select * from students where id = %s",(student_id,)
        # %s 쓰는 이유: 값을 sql문자열과 분리해서 전달하면 sql injection보안문제예방
        # , 붙이는 이유는 값이 한개인 튜플을 만들기 위해서.
    )

    student = cursor.fetchone() # fetchone:조회한 값 한 행만 반환.
    #조회한 값이 없다면 None 반환

    cursor.close()
    conn.close()

    if student is None:
        raise HTTPException(
            status_code= 404,
            detail="그런 학생 없다"
        )

    return student

########## sql문 연결 전####################################################
# @app.post("/students",status_code=201, response_model=StudentResponse) #정상적으로 학생 생성하면,201반환.
# # response_model이 있어야 정해진 정보단 응답 가능.
# #클라이언트가 보낸 json 데이터를 studentcreate 모델에 맞게 검증하고 python 객체로 만듦
# def create_student(student: StudentCreate):
#     new_student = {
#         "id": max((s["id"] for s in students),default=0)+1,
#         "name": student.name,
#         "score": student.score,
#         "memo": "서버 내부용 정보"
#     }
#     students.append(new_student)

#     return new_student

######### sql문 연결 후
@app.post("/students",status_code=201,response_model=StudentResponse)
def create_student(student: StudentCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Insert into students(name,score) values (%s,%s)",(student.name,student.score))

    conn.commit() #데이터베이스의 변경 사항을 확정하는 코드

    new_student = {
        "id" : cursor.lastrowid, #sql이 알아서 관리함으로 직접 계산 필요 없음.
        "name": student.name,
        "score": student.score
    }
    cursor.close()
    conn.close()

    return new_student











#11.24 수정하기. put(all) patch(want part)
@app.put("/students/{student_id}")
def update_student(student_id:int,data:StudentCreate):
    #data: 어떤 내용을 수정할 것인가.
    for student in students:
        if (student["id"] == student_id):
            student["name"] = data.name
            student["score"] = data.score

            return student
        
    #422 에러는 studentcreate를 만족시키지 못했을 때 나온다.
    #404 에러는 찾는 값이 없을 때.
    #500 에러는 필수 응답 데이터누락or검증에 실패
    raise HTTPException(
        status_code= 404
    )

@app.patch("/students/{student_id}")
def patch_student(student_id:int,data:StudentUpdate):
    for student in students:
        if (student["id"] == student_id):

            if data.name is not None:
                student["name"] = data.name 

            if data.score is not None:
                student["score"] = data.score


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if (student["id"]==student_id):
            students.remove(student)

            return {"message: 학생 삭제 완료"}

    raise HTTPException(
        status_code= 404,
        detail="그런 학생 없다 임마"
    )


@app.get("/db-test")
def db_test():
    conn = get_connection()
    conn.close() #database연결 종료.

    return {"message": "MySQL 연결 성공"}