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
# 그래프 2. 장르 안에 영화 - 트리맵 (크기: 총 관객)
# ------------------------------------------------------------
st.header("2. 장르 안에 담긴 영화들 (총 관객 기준)")

fig_treemap = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>",
)
fig_treemap.update_layout(margin=dict(t=30, b=30, l=10, r=10))

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------
# 그래프 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3. 총 관객 수 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
)
fig_hist.update_traces(
    hovertemplate="총 관객 구간: %{x}<br>영화 수: %{y}편<extra></extra>",
)
fig_hist.update_layout(
    xaxis_title="총 관객(명)",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_hist, use_container_width=True)

# 대부분의 영화가 몰려 있는 구간과 가장 관객이 많은 영화 계산
bin_series = pd.cut(df["total_audi"], bins=30)
most_common_bin = bin_series.value_counts().idxmax()
top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info(
    f"영화 대부분은 총 관객 **{int(most_common_bin.left):,}명 ~ {int(most_common_bin.right):,}명** "
    f"구간에 몰려 있고, 가장 관객이 많은 영화는 **'{top_movie_row['movieNm']}'** "
    f"(총 관객 {int(top_movie_row['total_audi']):,}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 그래프 4. 개봉일 스크린수 vs 총 관객 - 산점도 (장르별 색)
# ------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객: %{y:,}명<extra></extra>",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객(명)",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------
# 그래프 5. 장르별 총 관객 상자 그림 (영화 10편 이상 장르만)
# ------------------------------------------------------------
st.header("5. 장르별 총 관객 분포 (10편 이상 장르)")

genre_movie_count = df["genre"].value_counts()
major_genres = genre_movie_count[genre_movie_count >= 10].index
df_major_genres = df[df["genre"].isin(major_genres)]

fig_box = px.box(
    df_major_genres,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
)
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객: %{y:,}명<extra></extra>",
)
fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객(명)",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------
# 그래프 6. 개봉일 스크린수 vs 총 관객 - 버블 그래프 (크기: 첫 주 관객)
# ------------------------------------------------------------
st.header("6. 개봉일 스크린수와 총 관객 (첫 주 관객 크기 반영)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    hover_name="movieNm",
    size_max=40,
)
fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명<extra></extra>"
    ),
)
fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객(명)",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------
# 그래프 7. 제작 국가 → 장르 선버스트 (크기: 영화 편수)
# ------------------------------------------------------------
st.header("7. 제작 국가별 장르 구성")

nation_genre_counts = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

fig_sunburst = px.sunburst(
    nation_genre_counts,
    path=["nation", "genre"],
    values="count",
)
fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>",
)
fig_sunburst.update_layout(margin=dict(t=30, b=30, l=10, r=10))

st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown("**💡 이 그래프로 알 수 있는 것:** ")
st.info("여기에 이 그래프를 보고 알게 된 점을 한 문장으로 적어 보세요.")
