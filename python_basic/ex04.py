# 연산자

# 연산자 우선순위
print((10 - 2) * 4 / 2)
# 우선순위가 높은 연산자가 먼저 연산된다.
# 우선순위가 같으면 왼쪽 -> 오른쪽으로 연산된다.
# () 소괄호가 우선순위가 가장 높다.

# 0. ()         소괄호
# 1. **         거듭제곱
# 2. * / // %   곱셈, 나눗셈
# 3. + -        덧셈, 뺄셈
# 4. == != < > <= >= 비교연산
# 5. not        부정로직
# 6. and        AND로직
# 7. or         OR로직
# 8. = += -=    대입(복합대입)

# ^  비트 XOR

print(10**3)  # 10 * 10 * 10
a = 5
b = 3
# 비교,논리 연산자는 연산의 결과가 항상 True/False이다.
print(a == b)  # 같은가?
print(a != b)  # 같지않은가?
print(a > b)  # 큰가
print(a < b)  # 작은가
print(a <= b)  # 같거나 작은가
print(a >= b)  # 같거나 큰가

# 논리연산자
print(True)
print(False)
print(not True)  # 논리부정
# and
print(True and True)  # 둘다 참일때만 참
print(True and False)
print(False and True)
print(False and False)
# or
print(True or True)
print(True or False)
print(False or True)
print(False or False)  # 둘다 거짓일때만 거짓
