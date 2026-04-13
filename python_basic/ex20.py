# ex29.py
# 판다스 pandas 라이브러리로 CSV파일 읽고 쓰기
# pandas : 데이터 분석에 특화된 라이브러리
#        : Data Frame 행열 2차원 데이터 처리에 유용함.
#        : 금융 시계열 데이터를 다루기 위해 만듦

# pandas 라이브러리 설치
# pip install pandas
# py -m pip install pandas
# pip list : 설치되어 있는 모듈 리스트

import pandas as pd  # pd라는 별명으로 사용한다.

# 딕셔너리를 데이터 프레임으로 변환한다.
data = {
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [30, 25, 35],
    "도시": ["서울", "부산", "수원"],
}
# 데이터프레임(Data Frame) 객체 생성
df = pd.DataFrame(data)
print(df)
