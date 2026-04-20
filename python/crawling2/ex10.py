import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# ── 페이지 설정 ──────────────────────────────────
st.set_page_config(
    page_title="Gemini 채팅",
    page_icon="✨",
    layout="centered",
)

# ── API 초기화 (세션당 1회) ───────────────────────
@st.cache_resource
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(".env 파일에 GEMINI_API_KEY가 없습니다.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_client()
google_search_tool = types.Tool(google_search=types.GoogleSearch())

# ── 세션 상태 초기화 ──────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []   # {"role": "user"|"assistant", "content": str, "sources": list}
if "history" not in st.session_state:
    st.session_state.history = []    # Gemini API용 Content 리스트

# ── 사이드바 ──────────────────────────────────────
with st.sidebar:
    st.title("설정")
    use_search = st.toggle("Google 검색 사용", value=True)
    st.caption("최신 정보가 필요한 질문에 자동으로 Google 검색을 활용합니다.")
    st.divider()

    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.caption(f"모델: gemini-2.5-flash")
    project_number = os.getenv("GOOGLE_PROJECT_NUMBER", "-")
    st.caption(f"프로젝트 번호: {project_number}")

# ── 헤더 ─────────────────────────────────────────
st.title("✨ Gemini 채팅앱")
st.caption("Gemini 2.5 Flash · Google Search 연동")
st.divider()

# ── 이전 대화 렌더링 ──────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("검색 출처"):
                for src in msg["sources"]:
                    st.markdown(f"- [{src['title']}]({src['uri']})")

# ── 입력 처리 ─────────────────────────────────────
if prompt := st.chat_input("메시지를 입력하세요..."):

    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini API 호출
    st.session_state.history.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )

    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            try:
                config = types.GenerateContentConfig(
                    tools=[google_search_tool] if use_search else [],
                )
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=st.session_state.history,
                    config=config,
                )
                reply = response.text

                # 검색 출처 추출
                sources = []
                if response.candidates:
                    metadata = response.candidates[0].grounding_metadata
                    if metadata and metadata.grounding_chunks:
                        seen = set()
                        for chunk in metadata.grounding_chunks:
                            if chunk.web and chunk.web.uri not in seen:
                                seen.add(chunk.web.uri)
                                sources.append({
                                    "title": chunk.web.title or chunk.web.uri,
                                    "uri": chunk.web.uri,
                                })

                st.session_state.history.append(
                    types.Content(role="model", parts=[types.Part(text=reply)])
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "sources": sources,
                })

                st.markdown(reply)
                if sources:
                    with st.expander(f"검색 출처 ({len(sources)}개)"):
                        for src in sources:
                            st.markdown(f"- [{src['title']}]({src['uri']})")

            except Exception as e:
                st.error(f"오류 발생: {e}")
                st.session_state.history.pop()
