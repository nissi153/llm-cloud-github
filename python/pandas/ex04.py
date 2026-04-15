# ex04.py
import pandas as pd
import matplotlib.pyplot as plt

# 파이썬 시각화 라이브러리 : 매트롯립 matplotlib
# pip install matplotlib

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False  # 음수 부호 하이픈(-)으로

df = pd.read_csv("./pandas/books.csv")
print(df.info())

grouped = df.groupby("카테고리")["가격"].mean()

# 카테고리별 평균 가격을 시각화
