# ex01.py
# sqlite3 파이썬 기본 라이브러리 (설치 필요 X)
# sqlite3 SQL은 MySQL과 90%정도 유사하다.

# SQlite 플러그인 : SQLite
# CTRL + SHIFT + P : SQLite 검색
# https://sqlitebrowser.org/ : DBeaver 유사

import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

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

cursor.executemany(
    "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
    [
        ("Alice", 20, "A"),
        ("Bob", 22, "B"),
        ("Carol", 21, "A"),
    ],
)

# MySQL : 오토커밋 / Oracel, sqlite3 : 수동커밋
conn.commit()

cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

conn.close()
