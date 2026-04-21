# ex02.py
# 채널 분석 : https://www.youtube.com/@chudongpark
# Youtube Data API - channels().list()

import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

CHANNEL_HANDLE = "chudongpark"

# forHandle로 정확한 채널 직접 조회
res = youtube.channels().list(
    part="snippet,statistics,brandingSettings,contentDetails,status,topicDetails",
    forHandle=CHANNEL_HANDLE
).execute()

channel_id = res["items"][0]["id"]

ch = res["items"][0]
snippet          = ch.get("snippet", {})
statistics       = ch.get("statistics", {})
branding         = ch.get("brandingSettings", {}).get("channel", {})
content_details  = ch.get("contentDetails", {})
status           = ch.get("status", {})
topic_details    = ch.get("topicDetails", {})

print("=" * 60)
print("          YouTube 채널 분석 결과")
print("=" * 60)

print("\n[ 기본 정보 ]")
print(f"  채널명          : {snippet.get('title')}")
print(f"  채널 ID         : {channel_id}")
print(f"  핸들            : {snippet.get('customUrl', 'N/A')}")
print(f"  개설일          : {snippet.get('publishedAt', 'N/A')[:10]}")
print(f"  국가            : {snippet.get('country', 'N/A')}")
print(f"  설명            :\n    {snippet.get('description', '').replace(chr(10), chr(10)+'    ')}")

print("\n[ 채널 통계 ]")
print(f"  구독자 수       : {int(statistics.get('subscriberCount', 0)):,} 명")
print(f"  총 조회수       : {int(statistics.get('viewCount', 0)):,} 회")
print(f"  동영상 수       : {int(statistics.get('videoCount', 0)):,} 개")
print(f"  구독자 비공개   : {statistics.get('hiddenSubscriberCount', False)}")

print("\n[ 브랜딩 설정 ]")
print(f"  채널 키워드     : {branding.get('keywords', 'N/A')}")
print(f"  채널 설명(브랜딩): {branding.get('description', 'N/A')}")
print(f"  기본 탭         : {branding.get('defaultTab', 'N/A')}")
print(f"  추천 채널 표시  : {branding.get('showRelatedChannels', 'N/A')}")

print("\n[ 재생목록 ]")
uploads_id = content_details.get("relatedPlaylists", {}).get("uploads", "N/A")
print(f"  업로드 재생목록 ID: {uploads_id}")

print("\n[ 채널 상태 ]")
print(f"  개인정보 보호   : {status.get('privacyStatus', 'N/A')}")
print(f"  장기 게시 가능  : {status.get('longUploadsStatus', 'N/A')}")
print(f"  어린이 채널     : {status.get('madeForKids', 'N/A')}")

print("\n[ 주제 카테고리 ]")
topic_ids = topic_details.get("topicCategories", [])
for t in topic_ids:
    print(f"  - {t.split('/')[-1].replace('_', ' ')}")

print("\n[ 썸네일 URL ]")
thumbnails = snippet.get("thumbnails", {})
for size, info in thumbnails.items():
    print(f"  {size:10s}: {info.get('url')}")

print("=" * 60)
