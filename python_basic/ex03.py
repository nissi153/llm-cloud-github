# 문자열 다루기
str = "Life is too short, You need Python."
print(str)

# 문자열을 여러줄로
str = """
Life is too short, 
You need Python.
"""

# 문자열 중간에 글자 ' "을 넣고 싶다.
print("Python's favorite food is")
print('Python"s favorite food is')

# 문자열 합치기
print("Python" + " is fun!")
print("Python" * 3)  # PythonPythonPython
print("=" * 50)  # 구분선

# 문자열 인덱싱
str = "Life is too short, You need Python."
print(str[0])
print(str[1])
print(str[-1])  # 끝에서 첫번째 문자
print(str[-2])

# 문자열 슬라이싱
print(str[0:4])  # 시작인덱스:끝인덱스-1
print(str[:4])
print(str[19:])  # 시작인덱스부터 끝까지
print(str[:])
print(str[19:-7])

# 문자열 데이터 바인딩(보간)
print("I eat %d apple" % 3)  # %d 10진수를 의미
print("I eat %d apple, I sell %d apple" % (3, 2))
print("%0.4f" % 3.142345432)  # 소숫점 4자리
print("%10.4f" % 3.142345432)  # 전체자릿수 10자리, 소숫점 4자리
print("%010.4f" % 3.142345432)  # 빈공간을 0으로 채우고 10자리

# 문자열 길이
a = "hobby"
print(len(a))  # 5

# 특정 문자의 갯수 찾기
print(a.count("b"))  # 2
print(a.count("v"))  # 0

a = "hobby"
# 특정 문자의 위치(인덱스) 찾기
print(a.find("b"))
print(a.find("b", a.find("b") + 1))  # 두번째 b의 위치
print(a.find("v"))  # 못찾으면 -1

# 구분자 넣기
a = ","
print(a.join("abcd"))  # a,b,c,d

# 양쪽 공백 없애기
a = " HI "
print(a.strip())

# 문자열 나누기 => 배열
a = "Life is too short"
print(a.split())  # ['Life', 'is', 'too', 'short']
a = "Life,is,too,short"
print(a.split(","))  # ['Life', 'is', 'too', 'short']

# 문자열 바꾸기
a = "Life is too short"
print(a.replace("Life", "Your leg"))
