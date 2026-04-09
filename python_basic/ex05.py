# 주요 데이터 타입 - 데이터를 담는 그릇

# 변수 Variable
#   숫자 Number
# 정수형 : int
from typing import Any, Literal


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

# 타입 힌트(Hint)
# 파이썬 3.5부터 지원, 코드 실행에는 영향이 없고, 가독성과 정적 분석
# 에 사용됨. AI가 맥락을 파악하고 정확한 코드를 생성하는데 도움.
# 대신 토큰을 더 많이 소비한다.
# (JavaScript => TypeScript AI가 더 정확)
# 정적타입 언어 : Java, C/C++, TS, Python+타입힌트
name: str = "홍길동"
age: int = 25
height: float = 175.5
is_good: bool = True

# 콜렉션 타입은 임포트해야 됨.
from typing import List, Dict, Tuple, Set

scores: List[int] = [70, 80, 90]
student: Dict[str, Any] = {"국어", 90, "영어", 80.5}
# Any : 어떤 타입이 들어와도 되는 타입(모든 타입)
#     : 자바 다형성(Object)
point: Tuple[int, int] = (10, 20)
fruits: Set[str] = {"사과", "배", "사과"}
