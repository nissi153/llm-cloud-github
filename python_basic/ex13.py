# ex13.py
# 딕셔너리 Dictionary( 사전 ) 영한사전 집(키) -> House(값)
# 키와 값의 쌍으로 이루어진 데이터 구조

# 빈 딕셔너리
empty_dict = {}
print(empty_dict)

person = {"name": "홍길동", "age": 30, "city": "한양"}
print(person)

print(person["name"])
print(person.get("name"))
print(person.get("address"))  # None
print(person.get("address", "주소값 없음"))

print(person.keys())
print(type(person.keys()))  # <class 'dict_keys'> 객체
print(list(person.keys()))

# 요소 삭제
del person["age"]
print(person)

# 전체 지우기
person.clear()
print(person)
