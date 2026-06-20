import streamlit as st
import random

# 1. 페이지 기본 설정 및 스타일 초기화
st.set_page_config(
    page_title="진로탐색을 위한 밸런스 게임!",
    page_icon="🌟",
    layout="wide"
)

# 커스텀 CSS: 보내주신 메인 화면의 블루&파스텔 톤 둥근 카드 레이아웃 재현
st.markdown("""
    <style>
    .main-header {
        background-color: #1E40AF;
        color: white;
        text-align: center;
        padding: 40px;
        border-radius: 25px;
        margin-bottom: 30px;
    }
    .main-header h1 { color: white; font-size: 2.5rem; margin-bottom: 10px; }
    .card-title { font-size: 1.8rem; font-weight: bold; margin-bottom: 15px; }
    .vs-text { font-size: 2rem; font-weight: bold; color: #F59E0B; text-align: center; margin-top: 15px; }
    .stButton>button {
        border-radius: 12px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 인공지능 시대 직업 데이터셋 (CEO, 개발자, 디자이너, PM, 데이터 사이언티스트 등)
JOB_DATA = {
    "IT & 인공지능 분야 🤖": [
        {"name": "AI 개발자 (인공지능 모델러)", "desc": "컴퓨터에게 사람처럼 생각하는 법을 가르치는 마법사!", "school": "광운인공지능고, 선린인터넷고"},
        {"name": "데이터 사이언티스트", "desc": "인터넷 속 데이터 뒤에 숨겨진 트렌드와 보물을 찾아내요.", "school": "선린인터넷고, 대동세무고"},
        {"name": "테크 PM (프로젝트 매니저)", "desc": "개발자, 디자이너와 소통하며 멋진 기술 서비스를 기획하고 총괄해요.", "school": "미래산업과학고, 서울디지텍고"}
    ],
    "디자인 & 스타트업 분야 🎨": [
        {"name": "UI/UX 디자이너", "desc": "스마트폰 앱을 쓸 때 가장 편리하고 예쁜 화면과 경험을 설계해요.", "school": "홍익디자인고, 예일디자인고"},
        {"name": "스타트업 CEO (창업가)", "desc": "인공지능 시대의 불편함을 해결할 새로운 비즈니스를 개척해요.", "school": "대동세무고, 서울디지텍고"}
    ]
}

# 3. 세부 게임 세션 상태 초기화 (문법 오류 수정)
if "step" not in st.session_state:
    st.session_state.step = 0
if "selected_field" not in st.session_state:
    st.session_state.selected_field = None
if "game_jobs" not in st.session_state:
    st.session_state.game_jobs = []
if "score" not in st.session_state:
    st.session_state.score = {}
if "soccer_score" not in st.session_state:
    st.session_state.soccer_score = 0
if "soccer_msg" not in st.session_state:
    st.session_state.soccer_msg = "공을 차서 골을 넣어보세요!"

# 4. 좌측 사이드바 내비게이션 구성 (이미지 화면과 매칭)
menu =
