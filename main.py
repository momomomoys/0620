import streamlit as st
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="홍익디자인고 입학설명회",
    page_icon="🎨",
    layout="wide"
)

# --- 커스텀 CSS (여학생 취향 저격 스타일링) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nanum Gothic', sans-serif;
        background-color: #FFF5F7; /* 연한 핑크 배경 */
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        border: 2px solid #FFB6C1;
        background-color: white;
        color: #FF69B4;
        font-weight: bold;
        height: 3em;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #FFB6C1;
        color: white;
        transform: scale(1.05);
    }
    
    /* 말풍선 스타일 */
    .speech-bubble {
        position: relative;
        background: #FFFFFF;
        border: 3px solid #FFB6C1;
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    
    .speech-bubble:after {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        width: 0;
        height: 0;
        border: 20px solid transparent;
        border-right-color: #FFB6C1;
        border-left: 0;
        margin-top: -20px;
        margin-left: -20px;
    }
    
    h1 { color: #96000F; }
    h3 { color: #FF69B4; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 정의 ---
dept_data = {
    "교무기획부": {
        "char_msg": "안녕! 우리 학교의 핵심 전공 수업을 담당하는 곳이야! 시각디자인과와 영상애니메이션과의 멋진 커리큘럼을 짜주신단다.",
        "content": "- 시각디자인과: 광고, 편집, UI 디자인 코스\n- 영상애니메이션과: 만화, 영상, 캐릭터, 애니메이터 코스\n- 고교학점제에 따른 학생 맞춤형 교육과정 운영"
    },
    "교육연구부": {
        "char_msg": "공부만 하는 게 아냐! 책을 읽고 그림을 그리는 감성적인 활동이 가득해!",
        "content": "- 스토리텔링 일러스트 공모전 (독서+디자인 융합)\n- 독서신문 '하루면가' 발행\n- GTQ 포토샵/일러스트 자격증 방과후 학교 지원"
    },
    "학생안전복지부": {
        "char_msg": "즐거운 학교 생활의 중심! 우리 학교의 힙한 동아리들을 관리해!",
        "content": "- SPAM(창업 동아리): 직접 제품을 만들고 판매해봐!\n- 바이오메디컬 아트: 홍익대 연계 메디컬 일러스트 체험\n- 총 40개의 정규/자율 동아리 활동 지원"
    },
    "특성화정보부": {
        "char_msg": "최첨단 AI 기술로 디자인하는 법을 배울 수 있어! 너무 멋지지 않니?",
        "content": "- AI 미래 디자인 한마당 (Midjourney 등 생성형 AI 활용)\n- 서울시/전국 상업경진대회 참가 지원\n- 최신 사양의 실습실과 디자인 소프트웨어 제공"
    },
    "진로교육부": {
        "char_msg": "홍대 미대 가고 싶은 친구들 주목! 선배들의 합격 비결을 알려줄게.",
        "content": "- 홍익대학교 미술대학 진학 시 4년 전액 장학금!\n- 매년 7~10% 홍대 미대 진학 (최근 6년간 50명)\n- 1:1 맞춤형 진로진학 컨설팅 및 대학 탐방"
    },
    "취업부": {
        "char_msg": "해외로 나가고 싶은 친구들 손! 일본으로 떠나는 글로벌 현장학습이 기다려!",
        "content": "- 글로벌 현장학습: 일본(오사카, 교토) 디자인 직무 연수\n- 신한 커리어온, 넷마블 직무 교육 프로그램\n- 드림 성장 바우처 및 자격증 응시 수수료 지원"
    }
}

# --- 메인 화면 구성 ---
st.title("🎨 홍익디자인고 입학설명회")
st.subheader("홍이와 함께하는 부서별 활동 탐험!")

# 레이아웃 나누기 (캐릭터 영역 | 버튼 & 설명 영역)
col1, col2 = st.columns([1, 2])

# 세션 상태 초기화 (클릭된 부서 기억)
if 'selected_dept' not in st.session_state:
    st.session_state.selected_dept = "진로교육부"

with col1:
    # 캐릭터 이미지 (깃허브에 올린 이미지 경로 사용)
    # 이미지 파일이 없다면 placeholder 이미지로 대체됨
    st.image("https://via.placeholder.com/400x600.png?text=Cute+Character", use_container_width=True)
    
    # 캐릭터 말풍선
    msg = dept_data[st.session_state.selected_dept]["char_msg"]
    st.markdown(f"""
        <div class="speech-bubble">
            <p style="font-size: 18px; font-weight: bold; margin:0;">{msg}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.write("### 🏢 궁금한 부서를 클릭해봐!")
    
    # 버튼 그리드 (2열)
    btn_col1, btn_col2 = st.columns(2)
    depts = list(dept_data.keys())
    
    for i, dept in enumerate(depts):
        with btn_col1 if i % 2 == 0 else btn_col2:
            if st.button(dept):
                st.session_state.selected_dept = dept
                st.rerun()

    # 상세 내용 표시 영역
    st.divider()
    selected = st.session_state.selected_dept
    st.markdown(f"### 📍 {selected}에서 지원하는 활동")
    st.info(dept_data[selected]["content"])
    
    # 하단 팁
    st.warning("💡 입학설명회에 참여하면 가산점이 있다는 사실, 잊지 마!")

# --- 푸터 ---
st.markdown("---")
st.caption("© 2024 홍익디자인고등학교 교무기획부 | 홍대 미대 연계 특성화고")
