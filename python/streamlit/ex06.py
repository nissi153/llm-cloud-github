# ex06.py

# 공공 오픈API 서비스 사용해 보기
# 공공데이터 포털 data.go.kr
#   무료회원 가입 후 API 키 가져오기
# 기상청 단기예보 조회서비스를 이용한 날씨예보 웹앱을 만들자.
import requests
import os

API_KEY = "s5I5DjrOsW90zbtUl3x51cKgA7WFrpPQbtfXsawzS9TQN860Jzbtgu1y5RYKnIg2YTSZInv07fnr9nM6p+V7Eg=="
# URL = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

params = {
    "serviceKey": API_KEY,
    "pageNo": "1",
    "numOfRows": "10",
    "dataType": "JSON",
    "base_date": "20260416",
    "base_time": "1100",
    "nx": "55",  # 우리나라 전역을 1/N해서 가지는 인덱스
    "ny": "127",
}

print("🌤️ 기상청 API 호출 중...")
response = requests.get(URL, params=params)
print("✅ API 응답:")
print(response.json())
