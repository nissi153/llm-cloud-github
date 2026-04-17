# ex02.py
# sqlite3 CRUD 예제
import sqlite3

# students.db 파일에 연결한다. 파일이 없으면 자동으로 새로 만든다.
conn = sqlite3.connect("students.db")

# cursor는 SQL 명령을 실행할 때 사용하는 도구라고 생각하면 된다.
cursor = conn.cursor()

# students 테이블을 만든다.
# IF NOT EXISTS → 이미 테이블이 있으면 오류 없이 그냥 넘어간다.
# id는 자동으로 1씩 증가하는 고유 번호이다.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS students (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        age     INTEGER NOT NULL,
        grade   TEXT    NOT NULL
    )
"""
)
# 변경사항을 DB 파일에 저장한다.
conn.commit()


# ── CREATE (추가) ────────────────────────────────────────
def create(name, age, grade):
    # ? 는 자리 표시자이다. 아래 튜플 값이 순서대로 ? 에 들어간다.
    # 직접 문자열로 넣으면 SQL 인젝션 공격에 취약하므로 ? 를 사용한다.
    cursor.execute(
        "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
        (name, age, grade),
    )
    conn.commit()  # INSERT 후 반드시 commit 해야 저장된다.
    # cursor.lastrowid → 방금 추가된 행의 id 번호를 알려준다.
    print(f"[CREATE] {name} 추가 완료 (id={cursor.lastrowid})")


# ── READ (조회) ──────────────────────────────────────────
def read_all():
    # SELECT * → 테이블의 모든 컬럼을 가져온다.
    cursor.execute("SELECT * FROM students")
    # fetchall() → 조회된 모든 행을 리스트로 반환한다.
    rows = cursor.fetchall()
    print("[READ] 전체 목록:")
    for row in rows:
        # row = (id, name, age, grade) 순서이므로 row[1]이 이름이다.
        print(" ", row[1])
        print(" ", row[2])
        print(" ", row[3])


# ── UPDATE (수정) ────────────────────────────────────────
def update(student_id, name=None, age=None, grade=None):
    # 값이 전달된 항목만 골라서 수정한다.
    # WHERE id=? → 해당 id의 행만 수정한다. 없으면 전체가 바뀌므로 주의!
    if name:
        cursor.execute("UPDATE students SET name=? WHERE id=?", (name, student_id))
    if age:
        cursor.execute("UPDATE students SET age=? WHERE id=?", (age, student_id))
    if grade:
        cursor.execute("UPDATE students SET grade=? WHERE id=?", (grade, student_id))
    conn.commit()
    print(f"[UPDATE] id={student_id} 수정 완료")


# ── DELETE (삭제) ────────────────────────────────────────
def delete(student_id):
    # WHERE id=? → 해당 id의 행 하나만 삭제한다.
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    print(f"[DELETE] id={student_id} 삭제 완료")


# ── 실행 ─────────────────────────────────────────────────

# 학생 3명 추가
create("Alice", 20, "A")
create("Bob", 22, "B")
create("Carol", 21, "A")

# 추가 후 전체 목록 출력
read_all()

# Bob(id=2)의 학점을 "B" → "A" 로 수정
update(2, grade="A")
read_all()

# Carol(id=3) 삭제
delete(3)
read_all()

# 모든 작업이 끝나면 연결을 닫는다.
conn.close()
