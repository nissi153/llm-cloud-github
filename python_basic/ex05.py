# 주요 데이터 타입 - 데이터를 담는 그릇

# 변수 Variable
#   숫자 Number
# 정수형 : int
from typing import Literal


from turtle import st


age = 30
year = 2026
print(type(age))  # <class 'int'>
# 실수형 : float
pi = 3.141592
print(type(pi))  # <class 'float'>
# 복소수형 : complex
c1 = 3 + 4j  # 실수부 + 허수부
print(type(c1))  # <class 'complex'>
print(c1.real)
print(c1.imag)

#   문자열 String
string = "Hello, Python!"
print(type(string))  # <class 'str'>

# 리스트 List = 배열(리스트)
mylist = [1, 2, "hello", 3.14, True]
print(type(mylist))  # <class 'list'>
print(mylist[0])
mylist.append("new")
print(mylist)  # [1, 2, 'hello', 3.14, True, 'new']

# 튜플 Tuple = 길이가 고정된 리스트(함수반환값 리턴용)
#            = 변경불가
mytuple = (10, 20, "apple", False)
print(type(mytuple))
# <class 'tuple'>
# mytuple.append("NEW") # 지원불가
print(mytuple)

# 딕셔너리 Dictionary = Key:Value(JS 객체,Java Map,클래스)
dict_person = {"name": "Hong", "age": 30}
print(type(dict_person))  # <class 'dict'>
print(dict_person["name"])
print(dict_person.keys())  # ['name', 'age']
print(dict_person.values())  # ['Hong', 30]

# 세트 Set = 중복되지 않는 요소값
myset = {1, 2, 3, 2, 1}
print(myset)  # {1, 2, 3}

# 불리언 Boolean = 논리값
is_true = True

# 값없음 NoneType = 값없음을 알려줌.(Void, Null)
# 변수를 초기화할 때, 미리 알고 있는 값이 없으면, 타입을 모를때,
result = None
print(type(result))  # <class 'NoneType'>
if result == None:
    print("결과값 없음.")
