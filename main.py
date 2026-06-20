import streamlit as st
import random

# 1. 페이지 기본 설정 및 스타일 초기화
st.set_page_config(
    page_title="진로탐색을 위한 밸런스 게임!",
    page_icon="🌟",
    layout="wide"
)

# 커스텀 CSS: 메인 화면의 블루 & 파스텔 톤 둥근 카드 레이아웃 재현
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

# 2. 인공지능 시대 직업 데이터셋
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

# 3. 세부 게임 세션 상태 초기화
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

# 4. 좌측 사이드바 내비게이션 구성 (★ 이 부분의 줄바꿈과 수식을 한 줄로 명확히 수정했습니다)
menu = st.sidebar.radio("메뉴 선택", ["main", "진로", "축구게임"])

# ----------------- [ PAGE 1: main ] -----------------
if menu == "main":
    st.markdown("""
        <div class='main-header'>
            <h1>🌟 진로탐색을 위한 밸런스 게임!</h1>
            <p>밸런스 게임으로 진로탐색을 해보고 머리아프면 미니 게임도 즐겨보세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 🌋 1. 진로 밸런스 게임\n\n단 5~10개의 기가 막힌 밸런스 질문을 통해 당신의 비즈니스 성향을 날카롭게 분석합니다!\n\n**CEO, 개발자, 디자이너, PM, 데이터 사이언티스트** 중 젠슨 황과 가장 완벽한 케미를 자랑하는 당신의 천직을 확인해 보세요.")
        if st.button("🚀 밸런스 게임 시작하기", use_container_width=True):
            st.success("왼쪽 사이드바 메뉴에서 **'진로'**를 클릭하면 게임이 시작됩니다!")
            
    with col2:
        st.success("### ⚽ 2. 미니 축구 월드컵 게임\n\n머리 쓰는 진로 탐색에 지쳤다면? 짜릿한 스포츠 타임!\n\n간단하고 직관적인 컨트롤로 골문을 흔드는 실시간 미니 축구 게임입니다. 친구와 함께 혹은 혼자서 최고 점수에 도전하고 스트레스를 날려버리세요!")
        if st.button("⚽ 축구 게임 입장하기", use_container_width=True):
            st.success("왼쪽 사이드바 메뉴에서 **'축구게임'**을 클릭하여 입장해 주세요!")

# ----------------- [ PAGE 2: 진로 ] -----------------
elif menu == "진로":
    st.title("🌋 진로 밸런스 선택")
    
    if st.session_state.step == 0:
        st.markdown("#### 먼저 관심 있는 대분류 분야를 선택하세요!")
        fields = list(JOB_DATA.keys())
        cols = st.columns(len(fields))
        for i, field in enumerate(fields):
            with cols[i]:
                if st.button(field, key=f"field_{i}", use_container_width=True):
                    st.session_state.selected_field = field
                    pool = JOB_DATA[field] * 4
                    random.shuffle(pool)
                    st.session_state.game_jobs = pool[:10]  # 5단계 매칭을 위한 10개 확보
                    st.session_state.step = 1
                    st.rerun()

    elif 1 <= st.session_state.step <= 5:
        current_step = st.session_state.step
        st.write(f"### 🎮 {current_step} / 5 단계 진행 중")
        st.progress(current_step / 5)
        
        job_a = st.session_state.game_jobs[(current_step - 1) * 2]
        job_b = st.session_state.game_jobs[(current_step - 1) * 2 + 1]
        
        col1, v_col, col2 = st.columns([4, 1, 4])
        with col1:
            st.markdown(f"### 🅰️ {job_a['name']}")
            st.caption(job_a['desc'])
            if st.button("이게 더 좋아! 🅰️", key=f"btn_a_{current_step}", use_container_width=True):
                st.session_state.score[job_a['name']] = st.session_state.score.get(job_a['name'], 0) + 1
                st.session_state.step += 1
                st.rerun()
        with v_col:
            st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"### 🅱️ {job_b['name']}")
            st.caption(job_b['desc'])
            if st.button("이게 더 좋아! 🅱️", key=f"btn_b_{current_step}", use_container_width=True):
                st.session_state.score[job_b['name']] = st.session_state.score.get(job_b['name'], 0) + 1
                st.session_state.step += 1
                st.rerun()

    else:
        st.balloons()
        st.success("🎉 밸런스 게임 완료!")
        best_job = max(st.session_state.score, key=st.session_state.score.get) if st.session_state.score else "스타트업 CEO (창업가)"
        
        final_info = {"desc": "미래를 이끌어갈 인재", "school": "홍익디자인고 등 특성화고등학교"}
        for f in JOB_DATA:
            for j in JOB_DATA[f]:
                if j['name'] == best_job:
                    final_info = j
                    break
                    
        st.markdown(f"## 🏆 너의 추천 직업: **[{best_job}]**")
        st.write(f"✨ {final_info['desc']}")
        st.info(f"🏫 **추천 고등학교:** {final_info['school']}")
        
        if st.button("🔄 다시 테스트하기", use_container_width=True):
            st.session_state.step = 0
            st.session_state.score = {}
            st.rerun()

# ----------------- [ PAGE 3: 축구게임 ] -----------------
elif menu == "축구게임":
    st.title("⚽ 쉬어가는 미니 축구 게임")
    st.metric(label="현재 축구 점수", value=f"{st.session_state.soccer_score} 점")
    st.subheader(f"🥅 {st.session_state.soccer_msg}")
    
    st.write("---")
    cols = st.columns(3)
    
    with cols[0]:
        if st.button("📐 왼쪽 구석 슛", use_container_width=True):
            if random.choice([True, False]):
                st.session_state.soccer_msg = "🎉 골인! 구석을 완벽하게 찔렀습니다!"
                st.session_state.soccer_score += 10
            else:
                st.session_state.soccer_msg = "🧤 아쉽습니다! 골키퍼 선방에 막혔습니다."
            st.rerun()
            
    with cols[1]:
        if st.button("⚡ 정면 강슛", use_container_width=True):
            if random.choice([True, False]):
                st.session_state.soccer_msg = "🎉 골인! 골키퍼가 손도 못 댔습니다!"
                st.session_state.soccer_score += 10
            else:
                st.session_state.soccer_msg = "⚽ 쾅! 골대를 맞고 튕겨 나옵니다!"
            st.rerun()
            
    with cols[2]:
        if st.button("📐 오른쪽 구석 슛", use_container_width=True):
            if random.choice([True, False]):
                st.session_state.soccer_msg = "🎉 골인! 골키퍼 타이밍을 빼앗았습니다!"
                st.session_state.soccer_score += 10
            else:
                st.session_state.soccer_msg = "🧤 아쉽습니다! 골키퍼가 방향을 읽었습니다."
            st.rerun()
            
    if st.button("🔄 점수 초기화", key="reset_game"):
        st.session_state.soccer_score = 0
        st.session_state.soccer_msg = "공을 차서 골을 넣어보세요!"
        st.rerun()
