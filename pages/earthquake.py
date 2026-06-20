import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
from datetime import datetime

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="Global Earthquake Tracker",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌋 전세계 지진 실시간 시각화 웹앱")
st.markdown("USGS(미국지질조사국) API 데이터를 활용하여 전세계에서 발생한 지진을 실시간으로 시각화합니다.")

# 2. 사이드바 - 조건 선택
st.sidebar.header("🔍 필터 설정")

# 연도 선택 (현재 연도 기준 과거까지 선택 가능)
current_year = datetime.now().year
selected_year = st.sidebar.selectbox(
    "조회할 연도를 선택하세요",
    range(current_year, 2000, -1),
    index=0
)

# 최소 진도(Magnitude) 설정
min_magnitude = st.sidebar.slider("최소 진도 (Magnitude)", 0.0, 9.0, 4.5, 0.5)

# 3. USGS API 데이터 캐싱 및 로드
@st.cache_data(ttl=3600)  # 1시간 동안 결과 캐싱 (스트림릿 클라우드 성능 최적화)
def load_earthquake_data(year, min_mag):
    # 선택한 연도의 1월 1일부터 12월 31일까지 (올해라면 오늘 날짜까지)
    start_time = f"{year}-01-01"
    end_time = f"{year}-12-31" if year < current_year else datetime.now().strftime("%Y-%m-%d")
    
    # USGS API Endpoint (GeoJSON 포맷)
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "minmagnitude": min_mag,
        "limit": 2000 # 스트림릿 클라우드 과부하 방지를 위한 최대 데이터 제한
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # GeoJSON을 Pandas DataFrame으로 변환
        features = data['features']
        if not features:
            return pd.DataFrame()
            
        earthquakes = []
        for f in features:
            prop = f['properties']
            geom = f['geometry']
            earthquakes.append({
                "title": prop['title'],
                "mag": prop['mag'],
                "place": prop['place'],
                "time": pd.to_datetime(prop['time'], unit='ms'),
                "longitude": geom['coordinates'][0],
                "latitude": geom['coordinates'][1],
                "depth": geom['coordinates'][2]
            })
        return pd.DataFrame(earthquakes)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 데이터 로딩 애니메이션
with st.spinner("USGS에서 지진 데이터를 가져오는 중입니다..."):
    df = load_earthquake_data(selected_year, min_magnitude)

# 4. 메인 화면 데이터 시각화
if df.empty:
    st.warning("선택한 조건에 해당하는 지진 데이터가 없습니다.")
else:
    # 대시보드 상단 통계 수치
    col1, col2, col3 = st.columns(3)
    col1.metric("총 발생 건수", f"{len(df)} 건")
    col2.metric("최대 진도", f"M {df['mag'].max():.1f}")
    col3.metric("평균 진도", f"M {df['mag'].mean():.1f}")
    
    st.subheader(f"📍 {selected_year}년 지진 발생 위치 (진도 {min_magnitude} 이상)")
    
    # pydeck을 이용한 인터랙티브 지도 시각화 (진도가 높을수록 붉고 크게 표시)
    df['radius'] = (df['mag'] ** 3) * 10  # 진도에 따라 마커 크기 차등화
    
    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=1,
        pitch=0
    )
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.6,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=3,
        radius_max_pixels=40,
        line_width_min_pixels=1,
        get_position="[longitude, latitude]",
        get_radius="radius",
        get_fill_color="[mag * 40, 50, 255 - (mag * 25), 160]", # 진도가 높을수록 붉은색
        get_line_color=[0, 0, 0],
    )
    
    # 지도 출력 및 툴팁 설정
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "위치: {place}\n진도: M {mag}\n시간: {time}\n깊이: {depth}km"}
    ))
    
    # 5. 데이터 테이블 표시
    st.subheader("📊 상세 데이터 목록")
    st.dataframe(
        df[['time', 'mag', 'place', 'depth', 'latitude', 'longitude']].sort_values(by='time', ascending=False),
        use_container_width=True
    )
