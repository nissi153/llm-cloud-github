# ex05.py
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False  # 음수 부호 하이픈(-)으로

df = pd.read_csv("./pandas/books2.csv")
print(df.info())

# 카테고리별 도서 수 시각화

# 카테고리 컬럼에서 각 값이 몇번 등장했는지 카운트한 1차 배열
# 내림차순 정렬됨, 결측치는 제외됨.
# 반환값 Series[index=컬럼이름, value=빈도수]
category_counts = df["카테고리"].value_counts()
print(category_counts)  # Series
category_counts.plot(kind="bar", color="skyblue")
plt.title("카테고리별 도서 수")
plt.xlabel("카테고리")
plt.ylabel("도서 수")
plt.tight_layout()
plt.savefig("category_count.png")
plt.show()
