# ex03.py
# 네이버 뉴스 크롤링 by 셀레니엄

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://news.naver.com/section/105"

# 헤드라인 목록 UL의 id는 배포마다 접두사 이후 값이 달라지므로 접두사로 매칭
css_selector_ul = "ul[id^='_SECTION_HEADLINE_LIST_']"
css_selector_li_tmpl = "ul[id^='_SECTION_HEADLINE_LIST_'] > li:nth-child({n}) > div > div > div.sa_text > a"

driver = webdriver.Chrome()
driver.get(URL)

# 헤드라인 목록이 로드될 때까지 최대 15초 대기
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_ul))
)

print("=" * 50)
print("네이버 뉴스 IT/과학 헤드라인 TOP 5")
print("=" * 50)

for i in range(1, 6):
    selector = css_selector_li_tmpl.format(n=i)
    element = driver.find_element(By.CSS_SELECTOR, selector)
    title = element.text.strip()
    link = element.get_attribute("href")
    print(f"[{i}] {title}")
    print(f"    {link}")
    print()

driver.quit()
