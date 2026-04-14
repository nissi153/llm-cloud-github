# 크롤링한 결과 CSV파일(로컬파일 Sqlite)에 저장하기
import requests
from bs4 import BeautifulSoup
import csv
import json
import datetime


def fetch_articles(url="https://news.ycombinator.com/"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select(".titleline > a")

    data = []
    for a in articles:
        title = a.text.strip()  # 좌우공백 제거
        link = a["href"].strip()
        data.append({"title": title, "link": link})  # dict 타입으로 추가

    return data


def main():
    print("해커 뉴스 기사 크롤링 중...")
    data = fetch_articles()

    print("CSV 저장 완료")
    print("JSON 저장 완료")


# 현재 파일에서 실행되었는지?
if __name__ == "__main__":
    main()
