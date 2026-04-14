# ex10.py
# while()문

# 형식
# 반복변수 초기화
# while 조건식:
#   참일때 수행하는 수행문
#   반복변수 증감

# 5초 카운트 다운
count = 5
while count > 0:
    print(count)
    count -= 1
print("발사!")

# 무한루프에 빠지는 경우
# 1. 콘솔 화면을 클릭하고 CTRL + C로 빠져나온다.
# 2. 콘솔 세션을 종료(휴지통)한다.
# 3. VScode 코드를 꼈다 켠다.
# 4. 작업관리자에서 Python 프로세스를 끝내기 한다.
# 5. 컴퓨터의 OS를 꼈다 켠다.

# 무한루프 만들기 - 자판기,엘리베이터 프로그램
counter = 0
while True:
    counter += 1
    if counter > 10:
        break
    print(counter)
print("무한루프 종료")

# continue문
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

# 연습문제
# while문을 사용하여 사용자가 입력한 숫자의 자릿수를 세어서 출력하시오.
# 예시:
# 입력: 12345 → 출력: "5자리 숫자입니다"
# 입력: 789 → 출력: "3자리 숫자입니다"
# 힌트: 숫자를 10으로 나누면서 0이 될 때까지 반복
n: int = int(input("숫자 입력"))
length = 1
while True:
    n = n // 10
    if n == 0:
        break
    length += 1
print(f"{length}자리 숫자입니다.")
