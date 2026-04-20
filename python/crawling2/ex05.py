# ex05.py
# 인프런 강의 크롤링 → SQLite3 저장
# [테스트 모드] 첫 페이지 40개만 수집
#   - 목록 페이지: 기존 필드 + 강의 상세 URL
#   - 상세 페이지 방문:
#       · category1 / category2  (예: "개발 · 프로그래밍" / "풀스택")
#       · release_date           (가장 오래된 수강평 날짜 추정, 형식: "2024-05-26")

import sys
import io
import os
import sqlite3
import time
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

TOTAL_PAGES = 142        # 전체 페이지
LIMIT_PER_PAGE = 100     # 페이지당 상한 (실제로는 ~40)
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inflearn_courses.db")

# 사용자가 제공한 상세 페이지 카테고리 selector
CATEGORY_SELECTOR = (
    "#__next > div.css-zun3te.mantine-1fr50if > main > div "
    "> section.css-1pno9se.mantine-np9wqc > div > div "
    "> div.css-1fkgwz8.mantine-5n4x4z > div > div.css-2i1bjs.mantine-e3wuc0 "
    "> div.css-umsf7r.mantine-1avyp1d > div > div"
)


def page_url(n):
    if n == 1:
        return "https://www.inflearn.com/courses"
    return f"https://www.inflearn.com/courses?page_number={n}"


def scrape_page(driver, page_num):
    driver.get(page_url(page_num))
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article[class*='mantine-Card-root']")
            )
        )
    except TimeoutException:
        print(f"  [경고] 페이지 {page_num} 로딩 타임아웃 — 건너뜀")
        return []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
    time.sleep(1.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1.2)

    all_cards = driver.find_elements(By.CSS_SELECTOR, "article[class*='mantine-Card-root']")

    courses = []
    for card in all_cards:
        paras = card.find_elements(By.TAG_NAME, "p")
        if not paras or not paras[0].text.strip():
            continue

        title = paras[0].text.strip()
        author = paras[1].text.strip() if len(paras) > 1 else "-"

        # 강의 상세 URL — 카드 하위/상위 어디에 있든 탐색, 추천 트래킹 쿼리 제거
        href = "-"
        try:
            href = driver.execute_script("""
                const card = arguments[0];
                let link = card.querySelector('a[href*="/course/"]');
                if (link) return link.href;
                link = card.querySelector('a[href]');
                if (link) return link.href;
                let node = card.parentElement;
                while (node) {
                    if (node.tagName === 'A' && node.href) return node.href;
                    node = node.parentElement;
                }
                return null;
            """, card) or "-"
            if href != "-" and "?" in href:
                href = href.split("?", 1)[0]
        except Exception:
            pass

        try:
            img = card.find_element(By.CSS_SELECTOR, "picture img")
            thumbnail = img.get_attribute("src") or img.get_attribute("data-src") or "-"
        except Exception:
            thumbnail = "-"

        spans = card.find_elements(By.TAG_NAME, "span")
        subscriber = "-"
        for s in spans:
            text = s.text.strip()
            if text.endswith("+") and any(ch.isdigit() for ch in text):
                subscriber = text
                break

        p_texts = [p.text.strip() for p in paras]
        if len(p_texts) > 4 and "%" in p_texts[4]:
            original_price = p_texts[2] if len(p_texts) > 2 else "-"
            sale_price     = p_texts[5] if len(p_texts) > 5 else "-"
            rating         = p_texts[7] if len(p_texts) > 7 and p_texts[7] else "-"
            review_count   = p_texts[8] if len(p_texts) > 8 and p_texts[8].startswith("(") else "-"
        else:
            original_price = p_texts[2] if len(p_texts) > 2 else "-"
            sale_price     = original_price
            rating         = p_texts[4] if len(p_texts) > 4 and p_texts[4] else "-"
            review_count   = p_texts[5] if len(p_texts) > 5 and p_texts[5].startswith("(") else "-"

        # 무료 강의 제외
        if sale_price in ("무료", "-", ""):
            continue

        courses.append({
            "title":          title,
            "author":         author,
            "subscriber":     subscriber,
            "rating":         rating,
            "review_count":   review_count,
            "original_price": original_price,
            "sale_price":     sale_price,
            "thumbnail":      thumbnail,
            "url":            href,
        })

        if len(courses) >= LIMIT_PER_PAGE:
            break

    return courses


def extract_detail(driver, url):
    """상세 페이지에서 category1/2, release_date(가장 오래된 수강평 날짜) 추출. 진단 로그 포함."""
    cat1, cat2, release_date = "-", "-", "-"
    diag = []
    t0 = time.time()
    if not url or url == "-" or not url.startswith("http"):
        diag.append("invalid_url")
        return cat1, cat2, release_date, diag

    try:
        driver.get(url)
    except Exception as e:
        diag.append(f"nav_fail:{type(e).__name__}")
        return cat1, cat2, release_date, diag

    # 1) 카테고리
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.css-umsf7r.mantine-1avyp1d")
            )
        )
        anchors = driver.find_elements(
            By.CSS_SELECTOR,
            "div.css-umsf7r.mantine-1avyp1d a[href*='/courses/']"
        )
        texts = [a.text.strip() for a in anchors if a.text.strip()]
        diag.append(f"cat_anchors={len(texts)}")
        if len(texts) >= 2:
            cat1, cat2 = texts[0], texts[1]
        elif len(texts) == 1:
            cat1 = texts[0]
    except Exception as e:
        diag.append(f"cat_fail:{type(e).__name__}")

    # 2) 출시일
    try:
        try:
            review_section = driver.find_element(
                By.CSS_SELECTOR, "section.css-1h0915r.mantine-1avyp1d"
            )
        except Exception as e:
            diag.append(f"rsec_miss:{type(e).__name__}")
            raise
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", review_section)
        time.sleep(1.0)
        diag.append("rsec_ok")

        # (a) 정렬 드롭다운 → "최신순"
        trigger = None
        for xpath in (
            ".//input[@value='추천순']",
            ".//button[.//text()[contains(., '추천순')]]",
            ".//*[self::div or self::span][normalize-space(text())='추천순']",
        ):
            try:
                el = review_section.find_element(By.XPATH, xpath)
                if el.is_displayed():
                    trigger = el
                    break
            except Exception:
                continue
        if trigger is not None:
            try:
                trigger.click()
            except Exception:
                driver.execute_script("arguments[0].click();", trigger)
            time.sleep(0.7)
            try:
                option = driver.find_element(
                    By.XPATH, "//*[normalize-space(text())='최신순']"
                )
                option.click()
                time.sleep(1.8)
                diag.append("sort=latest")
            except Exception as e:
                diag.append(f"sort_opt_fail:{type(e).__name__}")
        else:
            diag.append("sort_trigger_none")

        # (b) '더보기' 버튼 최대 3번만 클릭
        more_clicks = 0
        for _ in range(3):
            try:
                more_btns = [
                    b for b in review_section.find_elements(
                        By.XPATH, ".//button[contains(., '더보기')]"
                    )
                    if b.is_displayed()
                ]
            except Exception:
                try:
                    review_section = driver.find_element(
                        By.CSS_SELECTOR, "section.css-1h0915r.mantine-1avyp1d"
                    )
                    continue
                except Exception:
                    break
            if not more_btns:
                break
            btn = more_btns[0]
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.25)
            try:
                btn.click()
            except Exception:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    break
            time.sleep(0.7)
            more_clicks += 1
        diag.append(f"more={more_clicks}")

        # (c) 섹션 내 모든 날짜 수집 → 최소값
        try:
            text = review_section.text
        except Exception:
            review_section = driver.find_element(
                By.CSS_SELECTOR, "section.css-1h0915r.mantine-1avyp1d"
            )
            text = review_section.text
        matches = re.findall(r"(20\d{2})[.\-]\s*(\d{1,2})[.\-]\s*(\d{1,2})", text)
        diag.append(f"dates={len(matches)}")
        dates = set()
        for y, m, d in matches:
            mi, di = int(m), int(d)
            if 1 <= mi <= 12 and 1 <= di <= 31:
                dates.add(f"{int(y):04d}-{mi:02d}-{di:02d}")
        if dates:
            release_date = min(dates)
    except Exception as e:
        diag.append(f"rel_fail:{type(e).__name__}")

    diag.append(f"t={time.time()-t0:.1f}s")
    return cat1, cat2, release_date, diag


# ===== SQLite 초기화 (DB 전체 초기화) =====
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS courses")
cur.execute("""
    CREATE TABLE courses (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        page           INTEGER,
        rank_in_page   INTEGER,
        title          TEXT,
        author         TEXT,
        subscriber     TEXT,
        rating         TEXT,
        review_count   TEXT,
        original_price TEXT,
        sale_price     TEXT,
        thumbnail      TEXT,
        url            TEXT,
        category1      TEXT,
        category2      TEXT,
        release_date   TEXT
    )
""")
conn.commit()

# ===== 크롤링 =====
driver = webdriver.Chrome()
total_count = 0

try:
    for page in range(1, TOTAL_PAGES + 1):
        print(f"\n[{page}/{TOTAL_PAGES}] 목록 수집 중...")
        courses = scrape_page(driver, page)
        print(f"  → {len(courses)}개 발견. 상세 페이지 순회 시작.")

        for rank, c in enumerate(courses, start=1):
            print(f"  [{rank:>2}/{len(courses)}] {c['title'][:35]}...", flush=True)
            cat1, cat2, release_date, diag = extract_detail(driver, c["url"])
            print(f"      url={c['url']}")
            print(f"      cat=({cat1}/{cat2}) 출시일={release_date}")
            print(f"      diag={'|'.join(diag)}")

            cur.execute("""
                INSERT INTO courses
                (page, rank_in_page, title, author, subscriber, rating,
                 review_count, original_price, sale_price, thumbnail,
                 url, category1, category2, release_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (page, rank, c["title"], c["author"], c["subscriber"],
                  c["rating"], c["review_count"], c["original_price"],
                  c["sale_price"], c["thumbnail"], c["url"],
                  cat1, cat2, release_date))
            conn.commit()
            total_count += 1
finally:
    driver.quit()
    conn.close()

print("\n" + "=" * 60)
print(f"완료: {DB_FILE}")
print(f"이번 실행에서 {total_count}개 강의 저장")
print("=" * 60)
