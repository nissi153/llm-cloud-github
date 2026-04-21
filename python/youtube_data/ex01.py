# ex01.py
# .env : API KEY
# Youtube Data API Key : 활성화
# 구글트렌트(실시간인기검색어 24시간)
# 인기채널 분석(플레이보드, 민인터 사이트)

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

try:
    youtube = build("youtube", "v3", developerKey=api_key)
    response = youtube.videos().list(part="snippet", chart="mostPopular", maxResults=1).execute()
    print("API Key 활성화 확인!")
    print("인기 동영상 제목:", response["items"][0]["snippet"]["title"])
except Exception as e:
    print("API Key 오류:", e)
