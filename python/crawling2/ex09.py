import os
import sys
import csv
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("오류: .env 파일에 GEMINI_API_KEY가 없습니다.")
    exit(1)

client = genai.Client(api_key=api_key)

# CSV 파일 경로 설정
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "pandas", "books2.csv")

def load_csv(path: str) -> tuple[list[dict], str]:
    """CSV를 읽어 딕셔너리 리스트와 텍스트 형태로 반환"""
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    lines = [",".join(rows[0].keys())]
    for row in rows:
        lines.append(",".join(row.values()))
    csv_text = "\n".join(lines)

    return rows, csv_text

def build_summary(rows: list[dict]) -> str:
    """데이터 기본 통계 요약 문자열 생성"""
    prices = [int(r["가격"]) for r in rows]
    categories = {}
    authors = {}
    for r in rows:
        categories[r["카테고리"]] = categories.get(r["카테고리"], 0) + 1
        authors[r["저자"]] = authors.get(r["저자"], 0) + 1

    top_cat = max(categories, key=categories.get)
    top_author = max(authors, key=authors.get)

    return (
        f"총 도서 수: {len(rows)}권 | "
        f"평균 가격: {sum(prices)//len(prices):,}원 | "
        f"최고가: {max(prices):,}원 | 최저가: {min(prices):,}원 | "
        f"최다 카테고리: {top_cat}({categories[top_cat]}권) | "
        f"최다 저자: {top_author}({authors[top_author]}권)"
    )

# CSV 로드
try:
    rows, csv_text = load_csv(CSV_PATH)
except FileNotFoundError:
    print(f"오류: CSV 파일을 찾을 수 없습니다.\n경로: {os.path.abspath(CSV_PATH)}")
    exit(1)

summary = build_summary(rows)

# 시스템 프롬프트: CSV 데이터를 Gemini에 주입
system_prompt = f"""당신은 도서 데이터 분석 전문가입니다.
아래 CSV 데이터를 기반으로 사용자의 질문에 한국어로 정확하게 답해주세요.
통계, 비교, 필터링, 추천 등 다양한 분석 요청을 처리할 수 있습니다.

[CSV 데이터]
{csv_text}

[기본 통계]
{summary}
"""

history = []

print("=" * 50)
print("  도서 데이터 분석 챗봇 (books2.csv)")
print("=" * 50)
print(f"  {summary}")
print("=" * 50)
print("  질문 예시:")
print("    - 가장 비싼 책은?")
print("    - 인공지능 카테고리 책을 알려줘")
print("    - 홍길동이 쓴 책 목록과 평균 가격은?")
print("    - 카테고리별 평균 가격을 비교해줘")
print("  종료: 'exit' 또는 'quit'")
print("=" * 50)

while True:
    user_input = input("\n질문: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ("exit", "quit"):
        print("프로그램을 종료합니다.")
        break

    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )

        reply = response.text
        history.append(types.Content(role="model", parts=[types.Part(text=reply)]))
        print(f"\n분석 결과:\n{reply}")

    except Exception as e:
        print(f"오류 발생: {e}")
        history.pop()
