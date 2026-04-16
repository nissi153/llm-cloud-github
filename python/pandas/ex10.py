import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# pip install seaborn
# py -m pip install seaborn

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("./pandas/books2.csv")

# violinplot : 박스플롯 + 커널밀도추정을 결합한 차트

plt.figure(figsize=(8, 5))
sns.violinplot(x="카테고리", y="가격", data=df)
plt.title("카테고리별 가격 분포 (Violinplot)")
plt.tight_layout()
plt.savefig("violinplot.png")
plt.show()
