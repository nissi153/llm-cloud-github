import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding="utf-8")

URL = "https://finance.naver.com/news/mainnews.naver"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_top_news(n=5):
    response = requests.get(URL, headers=HEADERS)
    response.encoding = "euc-kr"
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select(".articleSubject a")[:n]:
        title = item.get_text(strip=True)
        href = item["href"]

        params = parse_qs(urlparse(href).query)
        article_id = params.get("article_id", [""])[0]
        office_id = params.get("office_id", [""])[0]
        news_url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"

        results.append({"title": title, "url": news_url})

    return results


def main():
    news_list = fetch_top_news()
    for item in news_list:
        print(f'<a href="{item["url"]}" target="_blank">{item["title"]}</a>')


if __name__ == "__main__":
    main()
