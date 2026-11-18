

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


students = [
    {"name": "민수", "score": 85}, #[0]
    {"name": "지수", "score": 92}, #[1]
    {"name": "현우", "score": 78}  #[2]
] # 딕셔너리가 들어있는 리스트.

# 딕셔너리 삭제
who = input()
found = False

for student in students:
    if (who == student["name"]):
        students.remove(student) #현재 검사하고 있는 딕셔너리인 student를 students에서 삭제.
        #처음에 한 students.remove(student[who])는 
        #student["문자열"]이 되니까 말이 안됨. 리스트의 인덱싱은 오직 정수.
        #딕셔너리의 인덱스는 숫자와 key값(문자열) 가능
        #ex> students[1]["name"] 1인덱스의 key가 name인 value값.
        found = True
        print(f"{who}학생이 삭제되었습니다.")
        
        break
    
if found == False:
    print(f"{who}학생을 찾을 수 없습니다.")
    
print(students)







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
