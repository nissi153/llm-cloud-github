# ex03.py
# chudongpark 채널 전체 영상 목록 (롱폼 + 숏폼)
# Youtube Data API - playlistItems / videos

import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

CHANNEL_HANDLE = "chudongpark"

# ── 1. 채널 정보 및 업로드 재생목록 ID 가져오기 ──────────────────
ch_res = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    forHandle=CHANNEL_HANDLE
).execute()

ch          = ch_res["items"][0]
channel_id  = ch["id"]
uploads_id  = ch["contentDetails"]["relatedPlaylists"]["uploads"]
total_videos = int(ch["statistics"]["videoCount"])

print("=" * 70)
print(f"  채널 : {ch['snippet']['title']}  |  전체 영상 수 : {total_videos:,}개")
print("=" * 70)

# ── 2. 업로드 재생목록에서 모든 video_id 수집 ────────────────────
video_ids = []
next_page  = None

while True:
    pl_res = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_id,
        maxResults=50,
        pageToken=next_page
    ).execute()

    for item in pl_res["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    next_page = pl_res.get("nextPageToken")
    if not next_page:
        break

# ── 3. video_id 50개씩 묶어 상세 정보 조회 ───────────────────────
videos = []

for i in range(0, len(video_ids), 50):
    chunk = video_ids[i : i + 50]
    v_res = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(chunk)
    ).execute()
    videos.extend(v_res["items"])

# ── 4. 롱폼 / 숏폼 분류 (duration 60초 이하 → 숏폼) ─────────────
import re

def parse_duration_sec(duration: str) -> int:
    """ISO 8601 PT#M#S → 초"""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    h = int(m.group(1) or 0)
    mn = int(m.group(2) or 0)
    s = int(m.group(3) or 0)
    return h * 3600 + mn * 60 + s

def fmt_duration(sec: int) -> str:
    if sec < 60:
        return f"{sec}초"
    elif sec < 3600:
        return f"{sec // 60}분 {sec % 60}초"
    else:
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h}시간 {m}분 {s}초"

def best_thumbnail(thumbnails: dict) -> str:
    for key in ("maxres", "standard", "high", "medium", "default"):
        if key in thumbnails:
            return thumbnails[key]["url"]
    return "N/A"

longform  = []
shortform = []

for v in videos:
    sec = parse_duration_sec(v["contentDetails"]["duration"])
    (shortform if sec <= 60 else longform).append((v, sec))

# 업로드 날짜 최신순 정렬
longform.sort(key=lambda x: x[0]["snippet"]["publishedAt"], reverse=True)
shortform.sort(key=lambda x: x[0]["snippet"]["publishedAt"], reverse=True)

# ── 5. 출력 ──────────────────────────────────────────────────────
def print_videos(label: str, items: list):
    print(f"\n{'━' * 70}")
    print(f"  [{label}]  총 {len(items)}개")
    print(f"{'━' * 70}")
    for idx, (v, sec) in enumerate(items, 1):
        sn    = v["snippet"]
        st    = v["statistics"]
        vid   = v["id"]
        title = sn.get("title", "N/A")
        pub   = sn.get("publishedAt", "")[:10]
        thumb = best_thumbnail(sn.get("thumbnails", {}))
        views = int(st.get("viewCount", 0))
        likes = int(st.get("likeCount", 0))
        cmts  = int(st.get("commentCount", 0))
        dur   = fmt_duration(sec)
        tags  = ", ".join(sn.get("tags", [])[:5]) or "N/A"
        url   = f"https://www.youtube.com/watch?v={vid}"

        print(f"\n  {idx:>3}. {title}")
        print(f"       날짜     : {pub}")
        print(f"       길이     : {dur}")
        print(f"       조회수   : {views:,}  |  좋아요 : {likes:,}  |  댓글 : {cmts:,}")
        print(f"       태그     : {tags}")
        print(f"       썸네일   : {thumb}")
        print(f"       URL      : {url}")

print_videos("롱폼 영상", longform)
print_videos("숏폼 영상", shortform)

print(f"\n{'=' * 70}")
print(f"  총 {len(videos)}개  (롱폼 {len(longform)}개 / 숏폼 {len(shortform)}개)")
print(f"{'=' * 70}")
