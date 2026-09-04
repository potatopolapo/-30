import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)

    # genre 열에 세로막대(|) 기호로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    if "genre" in df.columns:
        df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # openDt(여덟 자리 숫자, 예: 20230115)를 날짜형으로 변환
    if "openDt" in df.columns:
        df["openDt"] = pd.to_datetime(
            df["openDt"].astype(str), format="%Y%m%d", errors="coerce"
        )

    return df


# ------------------------------------------------------------
# 제목 & 데이터 로드
# ------------------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    """
지난 1년간 박스오피스 10위권에 든 영화 가운데, 해당 기간에 개봉한 **216편**의 데이터를 살펴봅니다.
"""
)

try:
    df = load_data(DATA_URL)
except Exception as e:
    st.error(f"데이터를 불러오는 중 문제가 발생했습니다: {e}")
    st.stop()

with st.expander("📄 원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# 그래프 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------
# (추가 그래프를 위한 자리 - 필요에 따라 아래에 이어서 작성)
# ------------------------------------------------------------
# st.header("2. ...")
# ...
# st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
# st.info("여기에 문장을 적어 보세요.")
