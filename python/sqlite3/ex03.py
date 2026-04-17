# ex03.py
# students.db → students.csv 저장 예제
import sqlite3
import csv

# DB 파일에 연결한다.
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# students 테이블의 모든 행을 가져온다.
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# cursor.description 에는 컬럼(열) 정보가 들어 있다.
# 예) [('id', None, ...), ('name', None, ...), ('age', None, ...), ('grade', None, ...)]
# 각 항목의 첫 번째 값(인덱스 0)이 컬럼 이름이다.
headers = []
for col in cursor.description:
    col_name = col[0]  # 첫 번째 값만 꺼낸다 → 'id', 'name', 'age', 'grade'
    headers.append(col_name)  # 리스트에 하나씩 추가한다.

# students.csv 파일을 쓰기 모드로 연다.
# newline="" → csv 모듈이 줄바꿈을 직접 처리하도록 비워둔다.
# encoding="utf-8-sig" → 엑셀에서 한글이 깨지지 않도록 BOM을 포함한다.
with open("students.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    # 첫 번째 줄에 컬럼 이름(헤더)을 쓴다.
    writer.writerow(headers)

    # 나머지 줄에 데이터 행들을 쓴다.
    writer.writerows(rows)

print(f"저장 완료: students.csv ({len(rows)}행)")

conn.close()
