# ex11.py
# 원티드(wanted.co.kr) 채용 정보 크롤링 — Streamlit 앱

import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = "https://www.wanted.co.kr"

URL = (
    f"{BASE_URL}/wdlist/518"
    "?country=kr&job_sort=job.latest_order"
    "&years=0&years=2"
    "&locations=seoul.all&locations=gyeonggi.all"
    "&selected=872&selected=873&selected=660"
)

LIST_SELECTOR = "ul[class*='List_List']"
CARD_SELECTOR = f"{LIST_SELECTOR} li[class*='Card_Card']"
BOOKMARK_SELECTOR = "button[data-position-name]"


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)


def scroll_to_load(driver, pause=1.5, max_scrolls=5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_jobs():
    driver = create_driver()
    try:
        driver.get(URL)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CARD_SELECTOR))
        )
        scroll_to_load(driver)

        jobs = []
        for card in driver.find_elements(By.CSS_SELECTOR, CARD_SELECTOR):
            try:
                a_tag = card.find_element(By.CSS_SELECTOR, "a")
                href = a_tag.get_attribute("href") or ""
                if href.startswith("/"):
                    href = BASE_URL + href

                btn = card.find_element(By.CSS_SELECTOR, BOOKMARK_SELECTOR)
                title = btn.get_attribute("data-position-name") or ""
                company = btn.get_attribute("data-company-name") or ""

                if title and company and href:
                    jobs.append({"제목": title, "회사": company, "링크": href})
            except Exception:
                continue
        return jobs
    except TimeoutException:
        return []
    finally:
        driver.quit()


# ── UI ──────────────────────────────────────────────────
st.title("원티드 채용 정보")
st.caption("서울·경기 · 신입~2년 · 개발 직군")

if st.button("채용 정보 가져오기", type="primary"):
    with st.spinner("크롤링 중..."):
        jobs = get_jobs()

    if not jobs:
        st.error("채용 정보를 가져오지 못했습니다.")
    else:
        st.success(f"총 {len(jobs)}건")
        for job in jobs:
            st.markdown(f"**[{job['제목']}]({job['링크']})**  \n{job['회사']}")
            st.divider()
