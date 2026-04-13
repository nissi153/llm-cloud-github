# 파이썬 함수(function)

# 용도
# 1. 코드 중복 제거 - 코드 유지,보수에 중요!
# 2. 코드 재활용
# 3. 모듈화, 간격화


# 함수의 선언
def add(x, y):
    return x + y


# 함수 호출
print(add(10, 20))


# 매개변수 기본값
def show_msg(message, sender="익명"):
    print(f"{message} {sender}")


show_msg("안녕하세요?", "손님1")
show_msg("안녕하세요?")


# 가변 인자 리스트 : 매개변수가 여러개
def func_sum(*numbers):
    print(type(numbers))  # <class 'tuple'>
    sum = 0
    for num in numbers:
        sum += num
    return sum


print(func_sum(1, 2, 3))
print(func_sum(1, 2, 3, 4, 5, 6))


# 함수의 반환값 타입(타입 힌트 사용시)
def greeting(message: str) -> str:
    return f"{message}"


greeting("안녕하세요")
