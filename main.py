from fastapi import FastAPI , HTTPException
from pydantic import BaseModel,Field  #클라이언트가 보낸 데이터 검증.
#Field는 변수에 추가적인 데이터 검증 조건을 설정할 수 있게 해주는 기능.
import mysql.connector
import os
# 터미널에 작성하는 환경변수 변수
# $env:MYSQL_PASSWORD = Read-Host -MaskInput "MySQL password"
# 환경변수란? 운영체제의 실행 환경에 값을 저장해두고 프로그램에서 가져다 쓸 수      있도록  하는 변수.
#웹 요청을 처리할 프로그램을 준비하는 것
#cursor: 데베에 연결된 통로를 통해 sql을 실행하고 결과를 가져오는 작업자.

# 상태   코드의미	사용 상황
# 200	OK	       요청 성공
# 201	Created	   새로운 데이터 생성 성공
# 400	Bad Request	잘못된 요청
# 404	Not Found	데이터 없음
# 500	Internal Server Error	서버 내부 오류
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
# class 안의 내용물을 field라고 함.
class StudentCreate(BaseModel):
    name: str = Field(min_length=1,max_length=20)
    score: int = Field(ge=0,le=100) # 0이상, 100 이하
    department_id: int

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
    department_id: int | None
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


# # sql연결 후 get함수##################################################
# @app.get("/students")
# def get_students(min_score:int=0,max_score:int=100):
#     # 새로운 개념: query parameter: 아무것도 전달하지 않으면 0,100이 기본값.
#     # 값 전달은 url에서 할 수 있음.

#     if (min_score > max_score):
#         raise HTTPException( # raise가 실행되면 함수는 즉시 종료됨!!
#             status_code= 400, # 400 = 잘못된 요청.
#             detail="min>max입니다"
#         )
#     conn = get_connection() #mysql 연결
#     cursor = conn.cursor(dictionary=True) #sql명령을 실행할 객체 생성
#     # dctionary=True 딕셔너리 형태로 가져와라., false->value만 가져옴
#     # 딕셔너리 형태로 가져오면 컬럼이 붙어서 json응답을 만들기 편해짐.
#     cursor.execute("SELECT * FROM students \
#                     where score >= %s and score <= %s"
#                     ,(min_score,max_score)) #명령 실행
#     # 만약 min>max면(검색결과X) 빈 리스트를 반환.
#     # 이에 요청이 잘못됐다는 걸 알려주기 위해 raise~ 를 써야함
#     result = cursor.fetchall() #모든 행 가져오기

#     cursor.close()
#     conn.close() 

#     return {"students":result}

# @app.get("/students/{student_id}")
# def get_students(student_id:int):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#     #조회 결과를 dictionary로 받고싶어서  dictionary=True 붙임.
#     cursor.execute(
#         "select * from students where id = %s",(student_id,)
#         # %s 쓰는 이유: 값을 sql문자열과 분리해서 전달하면 sql injection보안문제예방
#         # , 붙이는 이유는 값이 한개인 튜플을 만들기 위해서.
#     )

#     student = cursor.fetchone() # fetchone:조회한 값 한 행만 반환.
#     #조회한 값이 없다면 fetchone가 None 반환

#     cursor.close()
#     conn.close()

#     if student is None:
#         raise HTTPException(
#             status_code= 404,
#             detail="그런 학생 없다"
#         )

#     return student

# ########## sql문 연결 전####################################################
# # @app.post("/students",status_code=201, response_model=StudentResponse) #정상적으로 학생 생성하면,201반환.
# # # response_model이 있어야 정해진 정보단 응답 가능.
# # #클라이언트가 보낸 json 데이터를 studentcreate 모델에 맞게 검증하고 python 객체로 만듦
# # def create_student(student: StudentCreate):
# #     new_student = {
# #         "id": max((s["id"] for s in students),default=0)+1,
# #         "name": student.name,
# #         "score": student.score,
# #         "memo": "서버 내부용 정보"
# #     }
# #     students.append(new_student)

# #     return new_student

# ######### sql문 연결 후
# @app.post("/students",status_code=201,response_model=StudentResponse)
# # 201은 created를 의미/미리 작성하는 이유: 학생을 새롭게 등록하는 요청이기 때문.
# # post요청이 성공적으로 처리됐을 때, 서버가 반환할 상태코드를 지정.(201=created)
# # studentresponse: 서버->클라이언트 응답 데이터를 검증,정리
# def create_student(student: StudentCreate):# create:클->서 요청 데이터 검증,정리
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("Insert into students(name,score) values (%s,%s)",(student.name,student.score))

#     conn.commit() #데이터베이스의 변경 사항을 확정하는 코드

#     new_student = {
#         "id" : cursor.lastrowid, #sql이 알아서 관리함으로 직접 계산 필요 없음.
#         "name": student.name,
#         "score": student.score
#     }
#     cursor.close()  
#     conn.close()

#     return new_student



# ############## sql 연결 전
# #11.24 수정하기. put(all) patch(want part)
# # @app.put("/students/{student_id}")
# # def update_student(student_id:int,data:StudentCreate):
# #     #data: 어떤 내용을 수정할 것인가.
# #     for student in students:
# #         if (student["id"] == student_id):
# #             student["name"] = data.name
# #             student["score"] = data.score

# #             return student
        
# #     #422 에러는 studentcreate를 만족시키지 못했을 때 나온다.
# #     #404 에러는 찾는 값이 없을 때.
# #     #500 에러는 필수 응답 데이터누락or검증에 실패
# #     raise HTTPException(
# #         status_code= 404
# #     )
# ############ sql 연결 후
# @app.put("/students/{student_id}")
# def update_student(student_id:int,data:StudentCreate):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("select * from students where id=%s",(student_id,))
#     student = cursor.fetchone()

#     if student is None:
#         cursor.close()
#         conn.close()
#         raise HTTPException(
#             status_code= 404,
#             detail="그런 학생 없습니다"
#         )

#     cursor.execute("update students set name=%s,score=%s where id = %s",
#                    (data.name,data.score,student_id))

#     conn.commit()

#     cursor.close()
#     conn.close()

#     return{"message":"수정 완료"}





# sql연결 전~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @app.patch("/students/{student_id}")
# def patch_student(student_id:int,data:StudentUpdate):
#     for student in students:
#         if (student["id"] == student_id):

#             if data.name is not None:
#                 student["name"] = data.name 

#             if data.score is not None:
#                 student["score"] = data.score


# #sql 연결 훗~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @app.patch("/students/{student_id}")
# def patch_student(student_id:int,data:StudentUpdate):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("select * from students where id=%s",(student_id,))

#     student = cursor.fetchone()

#     if (student is None):
#         cursor.close()
#         conn.close()

#         raise HTTPException(
#             status_code=404,
#             detail="그런 학생 없다고"
#         )
    
#     cursor.execute("update students set name=coalesce(%s,name), \
#                     score=coalesce(%s,score) where id=%s"
#                    ,(data.name,data.score,student_id))
#     #coalesce란? 전달받은 값이 null이면 기존값을 사용하고,
#     #null이 아니면 전달받은 값을 사용하는 sql함수
#     conn.commit()

#     cursor.close()
#     conn.close()

#     return {"message":"수정 완료"}
    


# sql 연결 전#####################################
# @app.delete("/students/{student_id}")
# def delete_student(student_id: int):
#     for student in students:
#         if (student["id"]==student_id):
#             students.remove(student)

#             return {"message: 학생 삭제 완료"}

#     raise HTTPException(
#         status_code= 404,
#         detail="그런 학생 없다 임마"
#     )



# # sql 연결 후#####################################
# @app.delete("/students/{student_id}")
# def delete_student(student_id:int):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("select * from students where id = %s",(student_id,))

#     student = cursor.fetchone()

#     if (student is None):
#         cursor.close()
#         conn.close()
#         raise HTTPException(
#             status_code=404,
#             detail="그런 학생 없다"
#         )

#     cursor.execute("delete from students where id = %s",(student_id,))

#     conn.commit()
#     cursor.close()
#     conn.close()

#     return {"message":"complete delete"}




@app.get("/db-test")
def db_test():
    conn = get_connection()
    conn.close() #database연결 종료.

    return {"message": "MySQL 연결 성공"}

@app.get("/students/departments")
def get_students_departments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT students.id,students.name,students.score,departments.department_name from students INNER join departments on students.department_id = departments.id;")
        # 문장이 너무 길어지면 삼중 따옴표로 하면 된다. """"ㅇㅇㄻㄴㄹㅇ""""
        find = cursor.fetchall()

        return find

    finally:
        cursor.close()
        conn.close()


@app.get("/students/department")
def get_students_by_department(department_id:int):
    conn = get_connection()
    cursor = conn.cursor(dictionary= True)

    cursor.execute("select * from departments where id = %s",(department_id,))

    department = cursor.fetchone()

    if (department_id is None):
        raise HTTPException(
            status_code=404,
            detail="그런 과 없습니다"
        )
    
    try:
        cursor.execute("""SELECT students.id,students.name,students.score,departments.department_name 
        from students 
        INNER join departments 
        on students.department_id = departments.id
        where departments.id = %s""",(department_id,))

        find = cursor.fetchall()
        #해당 과 사람이 없으면 빈 리스트 출력.200 출력.
        return {"students": find}
    
    finally:
        cursor.close()
        conn.close()


@app.get("/students/count")
def get_student_count():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""SELECT departments.department_name, count(students.id) as student_count
                        from departments
                        left join students
                        on departments.id = students.department_id
                        GROUP BY departments.id;""")
    # count(student.id)로 한 이유. null값은 세지 않기 위해서. 
    # count(*)하면 null값도 하나의 행으로 계산.
    # group by는 특정 컬럼의 값이 같은 행끼리 논리적으로 묶어주는 역할.
    # 그렇게 묶인 대상으로 count,sum,avg 같은 집계함수 사용.
        find = cursor.fetchall()

        return {"departments":find}

    finally:
        cursor.close()
        conn.close()










@app.get("/students")
def get_student(min_score:int=0, max_score:int =100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if (min_score> max_score):
        raise HTTPException(
            status_code=404,
            detail="min>max"
        )
    try:
        cursor.execute("select * from students where score>=%s and score<=%s",
                       (min_score,max_score))
        
        result = cursor.fetchall()
        
        return {"message":result}
    finally:
        cursor.close()
        conn.close()



#try-finally 구조.
@app.get("/students/{student_id}")
def get_student(student_id:int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try: #일단 실행할 코드를 작성하는 역할.
        cursor.execute("select * from students where id = %s",(student_id,))

        student = cursor.fetchone()

        if (student is None):
            raise HTTPException(
                status_code= 404,
                detail="그런 학생 없습니다"
            )

        return student

    # return 작동 전에 finally가 먼저 작동함.(finally->return)
    finally: # 위의 함수가 정상 종료되든, 예외가 발생하든 fianlly는 실행됨.
        cursor.close()
        conn.close()



@app.post("/students",status_code=201,response_model=StudentResponse)
def post_student(data:StudentCreate):
    conn = get_connection()
    cursor = conn.cursor()


    
    try:
        cursor.execute("select * from departments where id = %s",(data.department_id,))

        find = cursor.fetchone()

        if (find is None):
            raise HTTPException(
                status_code=400,
                detail="그런 학과 없습니다"
            )
        cursor.execute("insert into students(name,score,department_id) values (%s,%s,%s)"
                    ,(data.name,data.score,data.department_id))

        conn.commit()
        new_student = {
            "id": cursor.lastrowid,
            "name": data.name,
            "score": data.score,
            "department_id": data.department_id
        }
        return new_student
    
    finally:
        cursor.close()
        conn.close()



@app.put("/students/{student_id}")
def put_student(student_id:int,data: StudentCreate): #data에 요청으로 전달된 학생 정보가 들어감.
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("select * from students where id = %s",(student_id,))

        student = cursor.fetchone()

        if (student is None):
            raise HTTPException(
                status_code= 404,
                detail="그런 학생 없다"
            )
        
        cursor.execute("select * from departments where id = %s",(data.department_id,))

        department = cursor.fetchone()

        if ( department is None):
            raise HTTPException(
                status_code= 400,
                detail="그런 학과 없다"
            )

        cursor.execute("update students set name=%s,score=%s,department_id=%s where id = %s" \
                        ,(data.name,data.score,data.department_id, student_id))
        conn.commit()
        return {"id":student_id,
                "name":data.name,
                "score":data.score,
                "department_id":data.department_id
                }

    finally:
        cursor.close()
        conn.close()


@app.patch("/students/{student_id}")
def patch_student(student_id:int,data: StudentUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("select * from students where id = %s",(student_id,))
        
        student = cursor.fetchone()

        if (student is None):
            raise HTTPException(
                status_code=404,
                detail="No student"
            )

        cursor.execute("update students set name = coalesce(%s,name), \
                    score = coalesce(%s,score) where id = %s",
                    (data.name,data.score,student_id))
        conn.commit()

        return {"message":"부분 수정 완료"}

    finally:
        cursor.close()
        conn.close()


@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("select * from students where id=%s",(student_id,))

        student = cursor.fetchone()

        if (student is None):
            raise HTTPException(
                status_code=404,
                detail="no student"
            )
        
        cursor.execute("delete from students where id=%s",(student_id,))
        conn.commit()

        return {"message":"delete success"}

    finally:
        cursor.close()
        conn.close()


