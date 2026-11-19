

# student1 = {
#     "name": "민수",
#     "age": 20,
#     "score": 85
# }

# for i in student1: #딕셔너리 자체를 가져오면 value가 아니라 key값을 가져온다.
#     print(i)
#     #여기서 value의 값을 가져오고싶으면
#     print(student1[i])

# #key,value 동시 출력.
# for key, value in student1.items():
#     print(key,value)

#함수 안에 return은 함수 즉시 종료이므로, 밑의 줄들은 수행하지 않음.
#학생 이름을 검색하고 점수 또는 NOne를 반환. 오직 이 두가지 역할./ print는 함수 밖에서.
def find_score(name):
    for i in students: #for-else문 사용하기.
        if (i["name"] == name): #큰따옴표 반드시 넣기.
            return i["score"] #retuurn은 값을 반환하면서 함수 자체를 종료. 거의 break역할을 함.
    # else: #for문이 break 없이 끝났을 때 실행.
    #    return None
    return None


def add_student(name,score):
    for student in students:
        if (student["name"] == name): #딕셔너리에서 name을 꺼내서 확실히 비교를 해줘야함.
            return False
    #for 문이 끝나면 알아서 밑에 줄이 시작되니까 for-else문 쓸 필요가 없음.
    students.append({"name":name,"score":score}) 
    return True

def update_score(name,score):
    for student in students:
        if (student["name"] == name):
            student["score"] = score
            return True
    return False

def delete_student(name):
    for student in students:
        if (student["name"] == name):
            students.remove(student)
            return True
    return False


#고칠 점: return의 반환값을 사용해라!!!!!!!! 엄청나게 중요한 것임!!!!!!!!
#num==1, num==3
# 그래서 백엔드에서는 이런 식으로 역할을 나누는 습관이 중요해.
# - 함수: 데이터를 검색하고 결과를 반환한다.
# - 함수를 호출하는 코드: 반환된 결과를 어떻게 사용할지 결정한다.

students = [
    {"name": "민수", "score": 85}, #[0]
    {"name": "지수", "score": 92}, #[1]
    {"name": "현우", "score": 78}  #[2]
] # 딕셔너리가 들어있는 리스트.

while True:
    print("1. 학생추가\n2. 학생 조회\n3. 점수 수정\n4. 학생 삭제\n5. 종료")
    # print("메뉴를 선택하세요")
    # num = int(input())
    num = int(input("메뉴를 선택하세요: "))
    
    if (num==1):
        # print("학생 이름: ")
        # new = input() 이렇게 두줄로 말고.
        new = input("학생 이름: ")

        # print("추가할 학생 점수: ")
        # new_score = int(input())
        new_score = int(input("추가할 학생 점수: "))
        result = add_student(new, new_score)

        if result == True:
            print(f"{new} 학생을 추가하였습니다.")
        else:
            print("이미 등록된 학생입니다.")
        
    elif (num ==2 ):
        new = input("학생 이름: ")
        new_score = find_score(new)
        if (new_score is not None):
            print(f"{new}학생의 점수는 {new_score}점입니다.")
        else:
            print("없는 학생입니다.")
        
    elif (num == 3):
        print("수정할 학생 이름: ")
        new = input()
        print("수정할 학생 점수: ")
        new_score = int(input())        
        result = update_score(new,new_score)
        
        if (result == True):
            print(f"{new} 학생의 수정된 점수는 {new_score}점 입니다.")
        else:
            print("그런 학생 없습니다.")
        
    elif (num == 4):
        print("학생 이름: ")
        new = input()
        result = delete_student(new)
        if (result == True):
            print(f"{new}학생의 정보를 삭제했습니다.")
        else:
            print("이미 없는 학생입니다.")
    elif(num == 5):
        print("프로그램을 종료합니다.")
        break
        
print("최종 student의 형태")
print(students)


    
# 딕셔너리 삭제
# who = input()
# found = False

# for student in students:
#     if (who == student["name"]):
#         students.remove(student) #현재 검사하고 있는 딕셔너리인 student를 students에서 삭제.
#         #처음에 한 students.remove(student[who])는 
#         #student["문자열"]이 되니까 말이 안됨. 리스트의 인덱싱은 오직 정수.
#         #딕셔너리의 인덱스는 숫자와 key값(문자열) 가능
#         #ex> students[1]["name"] 1인덱스의 key가 name인 value값.
#         found = True
#         print(f"{who}학생이 삭제되었습니다.")
        
#         break
    
# if found == False:
#     print(f"{who}학생을 찾을 수 없습니다.")
    
# print(students)







#딕셔너리 추가
# who = input()
# score = int(input())
# found = False
# for student in students:
#     if (who == student["name"]):
#         print("이미 등록된 학생입니다.")
#         found = True
#         break
# if found == False:
#     students.append({"name":who,"score":score})
#     print(f"{who}학생이 등록되었습니다")






#학생 점수 수정하기
# who = input()
# new_score = int(input())
# found = False #found값 초기화 해줘야함. found는 그냥 변수지 함수가 아님.

# for student in students:
#     if (who == student["name"]):
#         student["score"] = new_score
#         print(f"{student['name']}학생의 점수가 {student['score']}점으로 수정되었습니다.")
#         found = True
#         break
# if found == False:
#     print("해당 학생을 찾을 수 없습니다.")
    

#학생 검색.
# name1 = input()
# for i in students: #for-else문 사용하기.
#     if (i["name"] == name1): #큰따옴표 반드시 넣기.
#         print(f"{i['name']}학생의 점수는 {i['score']}점 입니다")
#         break;
# else: #for문이 break 없이 끝났을 때 실행.
#     print("해당 학생을 찾을 수 없습니다.")

#found 사용하기!
#         found = True;
#         break;
    
# if found == False:
#     print("해당 학생을 찾을 수 없습니다.")

# found = True;
# break;

# if found == False:
#     print(!!!)
    
    
    
    
# for student in students: #students는 딕셔너리가 들어있는 리스트.
#     print(student["name"],student["score"])

# total = 0
# n = 0
# for student in students:
#     total += student["score"]
#     n += 1
# len(students) 하면 리스트의 총 길이 나옴. len(리스트이름), len(리스트이름), len(리스트이름)=리스트의 길이

# ave = total/n

#암기 print(f"문자열 {변수}") (f"문자열 {변수}")
# print(f"평균은 {ave:.2f}점 입니다.")

# print(f"학생 {len(students)}명의 평군 점수는 {ave}점 입니다.")
