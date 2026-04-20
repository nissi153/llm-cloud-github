import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
project_number = os.getenv("GOOGLE_PROJECT_NUMBER")

if not api_key:
    print("오류: .env 파일에 GEMINI_API_KEY가 없습니다.")
    exit(1)

client = genai.Client(api_key=api_key)

# Google Search 도구 설정
google_search_tool = types.Tool(google_search=types.GoogleSearch())

history = []

print("=" * 40)
print("  Gemini 콘솔 채팅앱 (Google Search)")
print(f"  프로젝트 번호: {project_number}")
print("  모델: gemini-2.5-flash")
print("  최신 정보는 Google 검색을 자동 활용")
print("  종료하려면 'exit' 또는 'quit' 입력")
print("=" * 40)

while True:
    user_input = input("\n나: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ("exit", "quit"):
        print("채팅을 종료합니다.")
        break

    history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=types.GenerateContentConfig(
                tools=[google_search_tool],
            ),
        )

        reply = response.text
        history.append(types.Content(role="model", parts=[types.Part(text=reply)]))
        print(f"\nGemini: {reply}")

        # 검색 출처 표시
        if response.candidates:
            metadata = response.candidates[0].grounding_metadata
            if metadata and metadata.grounding_chunks:
                print("\n[출처]")
                seen = set()
                for chunk in metadata.grounding_chunks:
                    if chunk.web and chunk.web.uri not in seen:
                        seen.add(chunk.web.uri)
                        title = chunk.web.title or chunk.web.uri
                        print(f"  - {title}")
                        print(f"    {chunk.web.uri}")

    except Exception as e:
        print(f"오류 발생: {e}")
        history.pop()
