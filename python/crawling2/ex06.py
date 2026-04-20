# ex06.py
# inflearn_courses.db 에서
#   1) 인기 강의 Top 10 (구독자순)
#     유용한IT학습(1~10)
#   2) 가장 돈 많이 번 강사 Top 10 (구독자수 × 할인가 합계)
#     300억~20억
#   3) 가장 인기있는 카테고리 ??
#   4) 최근 3개월에 가장 있는 강의는 ??
#       댓글의 가장 오래된 날짜? 7시간
#       댓글 내용(평판)을 분석(콘텐츠 분석)
# 를 조회하여 출력

import sys
import io
import os
import re
import sqlite3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "inflearn_courses copy.db")


def parse_subscriber(s):
    # "5,800+" → 5800, "-" → 0
    if not s or s == "-":
        return 0
    digits = re.sub(r"[^0-9]", "", s)
    return int(digits) if digits else 0


def parse_price(s):
    # "₩198,000" → 198000, "무료" / "-" → 0
    if not s or s in ("-", "무료"):
        return 0
    digits = re.sub(r"[^0-9]", "", s)
    return int(digits) if digits else 0


conn = sqlite3.connect(DB_FILE)
conn.create_function("parse_sub", 1, parse_subscriber)
conn.create_function("parse_price", 1, parse_price)
cur = conn.cursor()

# 1) 인기 강의 Top 10 (구독자순)
print("=" * 70)
print("인프런 인기 강의 Top 10 (구독자순)")
print("=" * 70)
cur.execute(
    """
    SELECT title, author, subscriber, sale_price
    FROM courses
    WHERE sale_price NOT IN ('무료', '-', '')
    ORDER BY parse_sub(subscriber) DESC
    LIMIT 10
"""
)
for i, (title, author, sub, price) in enumerate(cur.fetchall(), 1):
    print(f"{i:>2}. [{sub:>8}] {title}")
    print(f"     강사: {author} / 가격: {price}")

# 2) 가장 돈 많이 번 강사 Top 10 (구독자수 × 할인가 합계)
print()
print("=" * 70)
print("가장 돈 많이 번 강사 Top 10 (구독자수 × 할인가 합계 추정)")
print("=" * 70)
cur.execute(
    """
    SELECT author,
           SUM(parse_sub(subscriber) * parse_price(sale_price)) AS revenue,
           COUNT(*) AS course_count
    FROM courses
    WHERE author <> '-' AND author <> ''
      AND sale_price NOT IN ('무료', '-', '')
    GROUP BY author
    ORDER BY revenue DESC
    LIMIT 10
"""
)
for i, (author, revenue, cnt) in enumerate(cur.fetchall(), 1):
    print(f"{i:>2}. {author}")
    print(f"     추정 매출: ₩{revenue:,} / 강의 수: {cnt}개")

conn.close()
