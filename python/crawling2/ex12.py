# ex12.py
# ex06.py 를 스트림릿 앱으로 구현
# 실행: streamlit run ex12.py

import os
import re
import sqlite3
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "inflearn_courses.db")


def parse_subscriber(s):
    if not s or s == "-":
        return 0
    digits = re.sub(r"[^0-9]", "", s)
    return int(digits) if digits else 0


def parse_price(s):
    if not s or s in ("-", "무료"):
        return 0
    digits = re.sub(r"[^0-9]", "", s)
    return int(digits) if digits else 0


@st.cache_data
def load_courses():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM courses", conn)
    conn.close()
    df["sub_num"] = df["subscriber"].apply(parse_subscriber)
    df["price_num"] = df["sale_price"].apply(parse_price)
    df["revenue"] = df["sub_num"] * df["price_num"]
    return df


@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def generate_insight(topic: str, data_markdown: str, extra_context: str = "") -> str:
    client = get_gemini_client()
    if client is None:
        return "⚠️ GEMINI_API_KEY가 설정되지 않았습니다 (.env 확인)."
    prompt = f"""당신은 온라인 교육 시장 데이터 애널리스트입니다.
인프런(Inflearn) 강의 데이터의 '{topic}' 분석 결과가 아래와 같습니다.

{extra_context}

[데이터]
{data_markdown}

위 결과를 바탕으로 한국어로 3~5개의 핵심 인사이트를 불릿 포인트로 제시하세요.
- 숫자와 고유명사(강사명, 강의명, 카테고리)를 구체적으로 인용하세요.
- 시장 트렌드, 패턴, 주목할 만한 이상치(outlier)를 짚어주세요.
- 마지막에 '💡 추천/시사점' 한 줄을 덧붙이세요.
- 간결하되 근거가 보이게 작성하세요."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Gemini 호출 실패: {e}"


def render_insight_section(key: str, topic: str, data_markdown: str, extra: str = ""):
    with st.expander(f"🤖 {topic} AI 인사이트", expanded=False):
        cache_key = f"insight_{key}"
        if st.button("인사이트 생성", key=f"btn_{key}"):
            with st.spinner("Gemini 분석 중..."):
                st.session_state[cache_key] = generate_insight(
                    topic, data_markdown, extra
                )
        if cache_key in st.session_state:
            st.markdown(st.session_state[cache_key])
        else:
            st.caption("버튼을 누르면 Gemini가 위 데이터를 분석합니다.")


st.set_page_config(page_title="인프런 강의 분석", layout="wide")
st.title("📊 인프런 강의 분석 대시보드")
st.caption(f"DB: inflearn_courses.db / 기준일: {date.today().isoformat()}")

df = load_courses()

# 사이드바 필터
st.sidebar.header("⚙️ 필터")
all_authors = sorted(df["author"].dropna().unique().tolist())
default_excluded = [
    a for a in ["유용한IT학습", "인프런", "김영한", "Rookiss"] if a in all_authors
]
excluded_authors = st.sidebar.multiselect(
    "제외할 강사", all_authors, default=default_excluded
)
top_n = st.sidebar.slider("Top N", 10, 100, 30, step=5)
recent_months = st.sidebar.slider("최근 N개월 (Q4)", 1, 24, 6)

# 공통 필터 적용
paid = df[
    (~df["sale_price"].isin(["무료", "-", ""]))
    & (~df["author"].isin(excluded_authors))
    & (df["author"] != "-")
    & (df["author"] != "")
].copy()

tab1, tab2, tab3, tab4 = st.tabs(
    ["🏆 인기 강의", "💰 매출 강사", "📂 인기 카테고리", "🆕 최근 강의"]
)

# 1) 인기 강의 Top N
with tab1:
    st.subheader(f"인기 강의 Top {top_n} (구독자순)")
    top_courses = paid.nlargest(top_n, "sub_num")[
        ["title", "author", "subscriber", "sale_price", "release_date", "category1"]
    ].reset_index(drop=True)
    top_courses.index += 1
    top_courses.columns = ["강의명", "강사", "구독자", "가격", "출시일", "카테고리"]
    st.dataframe(top_courses, use_container_width=True, height=600)

    scatter_df = paid.nlargest(top_n, "sub_num").copy()
    scatter_df = scatter_df[scatter_df["price_num"] > 0]
    fig1 = px.scatter(
        scatter_df,
        x="price_num",
        y="sub_num",
        size="revenue",
        color="category1",
        hover_name="title",
        hover_data={"author": True, "release_date": True, "price_num": ":,", "sub_num": ":,"},
        labels={"price_num": "가격(원)", "sub_num": "구독자 수", "category1": "카테고리"},
        title=f"가격 × 구독자 버블 차트 (Top {top_n}, 크기=추정매출)",
        size_max=50,
    )
    fig1.update_layout(height=550)
    st.plotly_chart(fig1, use_container_width=True)

    render_insight_section(
        key="top_courses",
        topic="인기 강의 Top",
        data_markdown=top_courses.head(15).to_string(),
        extra=f"필터: 제외 강사 {excluded_authors or '없음'} / Top {top_n}",
    )

# 2) 매출 Top N 강사
with tab2:
    st.subheader(f"가장 돈 많이 번 강사 Top {top_n} (구독자수 × 할인가 합계)")
    agg = (
        paid.groupby("author")
        .agg(revenue=("revenue", "sum"), course_count=("title", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    agg.index += 1
    agg["추정 매출(억원)"] = (agg["revenue"] / 100_000_000).round(2)
    display = agg[["author", "추정 매출(억원)", "course_count"]].rename(
        columns={"author": "강사", "course_count": "강의 수"}
    )
    st.dataframe(display, use_container_width=True, height=600)

    treemap_df = display.head(30).copy()
    fig2 = px.treemap(
        treemap_df,
        path=[px.Constant("전체"), "강사"],
        values="추정 매출(억원)",
        color="추정 매출(억원)",
        color_continuous_scale="RdBu_r",
        hover_data={"강의 수": True},
        title=f"강사별 매출 점유 트리맵 (Top 30)",
    )
    fig2.update_traces(textinfo="label+value")
    fig2.update_layout(height=600)
    st.plotly_chart(fig2, use_container_width=True)

    render_insight_section(
        key="revenue",
        topic="매출 상위 강사",
        data_markdown=display.head(15).to_string(),
        extra=f"매출 = 구독자수 × 할인가 합계 추정 / 제외 강사: {excluded_authors or '없음'}",
    )

# 3) 인기 카테고리 Top 10
with tab3:
    st.subheader("가장 인기있는 카테고리 Top 10 (구독자 합계 기준)")
    cat_filtered = df[
        (~df["author"].isin(excluded_authors))
        & (df["category1"] != "-")
        & (df["category1"] != "")
    ]
    cat_agg = (
        cat_filtered.groupby("category1")
        .agg(total_sub=("sub_num", "sum"), course_count=("title", "count"))
        .reset_index()
        .sort_values("total_sub", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    cat_agg.index += 1
    cat_display = cat_agg.rename(
        columns={
            "category1": "카테고리",
            "total_sub": "총 구독자",
            "course_count": "강의 수",
        }
    )
    st.dataframe(cat_display, use_container_width=True)

    sunburst_df = cat_filtered[
        (cat_filtered["category2"] != "-") & (cat_filtered["category2"] != "")
    ]
    sun_agg = (
        sunburst_df.groupby(["category1", "category2"])
        .agg(total_sub=("sub_num", "sum"), course_count=("title", "count"))
        .reset_index()
    )
    fig3 = px.sunburst(
        sun_agg,
        path=["category1", "category2"],
        values="total_sub",
        color="total_sub",
        color_continuous_scale="Viridis",
        hover_data={"course_count": True},
        title="카테고리 계층 선버스트 (category1 → category2, 크기=구독자 합계)",
    )
    fig3.update_layout(height=650)
    st.plotly_chart(fig3, use_container_width=True)

    render_insight_section(
        key="category",
        topic="인기 카테고리",
        data_markdown=cat_display.to_string(),
        extra=f"구독자 합계 기준 / 제외 강사: {excluded_authors or '없음'}",
    )

# 4) 최근 N개월 인기 강의
with tab4:
    today = date.today()
    since = (today - timedelta(days=30 * recent_months)).isoformat()
    st.subheader(f"최근 {recent_months}개월 인기 강의 Top {top_n} (구독자순)")
    st.caption(f"기준: {since} ~ {today.isoformat()}")
    recent = (
        paid[(paid["release_date"] >= since) & (paid["release_date"] != "-")]
        .nlargest(top_n, "sub_num")[
            ["title", "author", "subscriber", "release_date", "category1"]
        ]
        .reset_index(drop=True)
    )
    recent.index += 1
    recent.columns = ["강의명", "강사", "구독자", "출시일", "카테고리"]
    st.dataframe(recent, use_container_width=True, height=600)

    render_insight_section(
        key="recent",
        topic=f"최근 {recent_months}개월 신규 인기 강의",
        data_markdown=recent.head(15).to_string(),
        extra=f"출시일 {since} ~ {today.isoformat()} / 제외 강사: {excluded_authors or '없음'}",
    )

# 하단 요약 지표
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("전체 강의 수", f"{len(df):,}")
col2.metric("필터 후 강의 수", f"{len(paid):,}")
col3.metric("고유 강사 수", f"{paid['author'].nunique():,}")
col4.metric("제외 강사", f"{len(excluded_authors)}명")
