import mysql.connector
import getpass
#Python은 사용자가 요청한 작업을 자동으로 처리하는 프로그램을 만드는 데 사용
#ex) 사용자가 웹사이트에서 자신의 이름을 입력하면 Python이 알아서 SQL을 실행

# 1. MySQL 서버 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass.getpass("MySQL 비밀번호: "),
    database="backend_study"
)

# 2. 커서 생성
cursor = conn.cursor()

# 3. UPDATE SQL 작성 (직접 작성!)
sql = "UPDATE students SET score = %s WHERE name = %s"
sql1 = "INSERT INTO students(name,score) VALUES (%s,%s)"
sql2 = "delete from students where name=%s"

# 4. SQL 실행 (직접 작성!) // mysql에 점수 수정 명령을 보낸 것.
# cursor.execute(sql,(100,"민수"))
# cursor.execute(sql1,("대만",99))
cursor.execute(sql2,("지수",))
# 5. 변경사항 확정 (직접 작성!)
conn.commit()


# 6. 변경된 학생 데이터 조회
cursor.execute("SELECT * FROM students")

# MYSQL에서 조회한 모든 데이터를 가져와서 변수 students에 저장한단 의미
students = cursor.fetchall()
#curosr: sql 명령을 실행하고 결과를 가져오는 객체
#fetchall() = sql 조회 결과의 모든 행을 가져오는 함수.
#students는 리스트.

# 7. 결과 출력
for student in students:
    print(student)

# 8. 연결 종료
cursor.close()
conn.close()