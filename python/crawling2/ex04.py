# ex04.py
# 인프런 사이트 크롤링 (React 동적 사이트 - Selenium 사용)
# 첫 페이지의 강의 목록 가져오기
# 수집 항목: 강의 제목, 저자(지식공유자), 구독자 수, 평점, 리뷰 수, 가격(정상가/할인가), 썸네일 URL
#
# [인프런 강의 카드 p 태그 구조]
# 할인 없음 (9개): [제목, 강사, 정상가, '', 평점, (리뷰), '', '', '']
# 할인 있음 (12개): [제목, 강사, 정상가, 이벤트문구, 할인율%, 할인가, '', 평점, (리뷰), ...]
# 구독자: span[1] 텍스트

import sys
import io
import csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://www.inflearn.com/courses"

driver = webdriver.Chrome()
driver.get(URL)

# 강의 카드가 로드될 때까지 최대 15초 대기
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "article[class*='mantine-Card-root']"))
)

# 스크롤을 내려 추가 강의 카드 로드 유도
driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
time.sleep(1.5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1.5)

# 모든 강의 카드 수집 (빈 ghost 카드 포함)
all_cards = driver.find_elements(By.CSS_SELECTOR, "article[class*='mantine-Card-root']")

# 제목이 있는 실제 카드만 필터링
courses = []
for card in all_cards:
    paras = card.find_elements(By.TAG_NAME, "p")
    if not paras or not paras[0].text.strip():
        continue  # 빈 ghost 카드 스킵

    # --- 제목 ---
    title = paras[0].text.strip()

    # --- 저자(지식공유자) ---
    author = paras[1].text.strip() if len(paras) > 1 else "-"

    # --- 썸네일 URL: src → data-src 순으로 확인 ---
    try:
        img = card.find_element(By.CSS_SELECTOR, "picture img")
        thumbnail = img.get_attribute("src") or img.get_attribute("data-src") or "-"
    except Exception:
        thumbnail = "-"

    # --- 구독자 수: 숫자+'+'로 끝나는 span 탐색 (New·배지 텍스트 제외) ---
    spans = card.find_elements(By.TAG_NAME, "span")
    subscriber = "-"
    for s in spans:
        text = s.text.strip()
        if text.endswith("+") and any(ch.isdigit() for ch in text):
            subscriber = text
            break

    p_texts = [p.text.strip() for p in paras]

    # --- 할인 여부 판단: p[4]에 '%' 포함 시 할인 적용 ---
    if len(p_texts) > 4 and "%" in p_texts[4]:
        # 할인 있음
        original_price = p_texts[2] if len(p_texts) > 2 else "-"
        sale_price     = p_texts[5] if len(p_texts) > 5 else "-"
        rating         = p_texts[7] if len(p_texts) > 7 and p_texts[7] else "-"
        review_count   = p_texts[8] if len(p_texts) > 8 and p_texts[8].startswith("(") else "-"
    else:
        # 할인 없음 (무료 포함)
        original_price = p_texts[2] if len(p_texts) > 2 else "-"
        sale_price     = original_price  # 정상가 = 판매가
        rating         = p_texts[4] if len(p_texts) > 4 and p_texts[4] else "-"
        review_count   = p_texts[5] if len(p_texts) > 5 and p_texts[5].startswith("(") else "-"

    courses.append({
        "title":          title,
        "author":         author,
        "subscriber":     subscriber,
        "rating":         rating,
        "review_count":   review_count,
        "original_price": original_price,
        "sale_price":     sale_price,
        "thumbnail":      thumbnail,
    })

driver.quit()

# ===== 결과 출력 =====
print("=" * 70)
print(f"인프런 강의 목록  (총 {len(courses)}개 강의)")
print("=" * 70)

for idx, c in enumerate(courses, start=1):
    print(f"\n[{idx:>3}] {c['title']}")
    print(f"      저자:   {c['author']}")
    print(f"      구독자: {c['subscriber']:>8}  |  평점: {c['rating']:>4}  |  리뷰: {c['review_count']}")
    print(f"      정상가: {c['original_price']:>10}  |  할인가: {c['sale_price']}")
    print(f"      썸네일: {c['thumbnail']}")

print("\n" + "=" * 70)
print(f"총 {len(courses)}개 강의 수집 완료")
print("=" * 70)

# ===== CSV 저장 =====
CSV_FILE = "inflearn_courses.csv"
fieldnames = ["번호", "제목", "저자", "구독자", "평점", "리뷰수", "정상가", "할인가", "썸네일URL"]

with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for idx, c in enumerate(courses, start=1):
        writer.writerow({
            "번호":       idx,
            "제목":       c["title"],
            "저자":       c["author"],
            "구독자":     c["subscriber"],
            "평점":       c["rating"],
            "리뷰수":     c["review_count"],
            "정상가":     c["original_price"],
            "할인가":     c["sale_price"],
            "썸네일URL":  c["thumbnail"],
        })

print(f"\nCSV 저장 완료 → {CSV_FILE}")
