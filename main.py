import streamlit as st
import random

# 1. 아기자기하고 화려한 스타일링을 위한 기본 세팅
st.set_page_config(
    page_title="내 미래를 찾아라! 직업 밸런스 게임",
    page_icon="🚀",
    layout="centered"
)

# 커스텀 CSS: 중학생 취향 저격 비비드&파스텔 테마
st.markdown("""
    <style>
    .main { background-color: #F9F7FI; }
    h1 { color: #FF6B6B; text-align: center; font-family: 'Nanum Gothic', sans-serif; }
    .sub-title { color: #4D96FF; text-align: center; font-size: 1.2rem; font-weight: bold; margin-bottom: 20px; }
    .stButton>button {
        background: linear-gradient(135deg, #6BCB77 0%, #4D96FF 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 20px;
        padding: 20px;
        border: none;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
    }
    .vs-text { font-size: 2rem; font-weight: bold; color: #FFD93D; text-align: center; margin-top: 15px; }
    </style>
""", unsafe_scale=True)

# 2. 인공지능 시대 유망 직종 위주의 트렌디한 데이터셋 (샘플링)
# 실제 서비스 시 커리어넷 API(https://www.career.go.kr/cnet/front/openapi/jobs.json) 결과를 매핑하여 확장 가능합니다.
JOB_DATA = {
    "IT & 인공지능 분야 🤖": [
        {"name": "AI 모델러 (인공지능 개발자)", "desc": "컴퓨터에게 사람처럼 생각하는 법을 가르치는 AI 마법사!", "school": "미래산업과학고, 서울디지텍고, 광운인공지능고"},
        {"name": "자율주행 모빌리티 전문가", "desc": "운전자가 없어도 안전하게 달리는 자동차와 드론을 설계해요.", "school": "경기자동차과학고, 용산철도고"},
        {"name": "메타버스 크리에이터", "desc": "가상현실 공간 속에 멋진 세상과 아바타 옷을 만들어요.", "school": "홍익디자인고, 서울영상고, 한강미디어고"},
        {"name": "화이트 해커 (사이버 보안관)", "desc": "나쁜 해커들로부터 소중한 정보와 시스템을 지켜냅니다.", "school": "선린인터넷고, 한세사이버보안고"},
        {"name": "데이터 사이언티스트", "desc": "인터넷 속 수많은 데이터 뒤에 숨겨진 보물을 찾아내요.", "school": "대동세무고, 선린인터넷고"}
    ],
    "디자인 & 미디어 분야 🎨": [
        {"name": "UI/UX 디자이너", "desc": "스마트폰 앱을 쓸 때 가장 편리하고 예쁜 화면을 디자인해요.", "school": "홍익디자인고, 예일디자인고, 서울디자인고"},
        {"name": "3D 영상 그래픽 디자이너", "desc": "영화나 게임 속에 나오는 화려한 3D 캐릭터와 효과를 만들어요.", "school": "홍익디자인고, 한국애니메이션고"},
        {"name": "콘텐츠 크리에이터 (영상 편집자)", "desc": "유튜브, 틱톡 등 사람들의 시선을 사로잡는 영상을 기획하고 편집해요.", "school": "서울영상고, 한강미디어고"},
        {"name": "이모티콘 프로듀서", "desc": "메신저에서 매일 쓰는 귀여운 캐릭터와 감정을 창조해요.", "school": "홍익디자인고, 성동글로벌경영고"}
    ],
    "바이오 & 환경 로봇 분야 🌱": [
        {"name": "로봇 공학자", "desc": "인간을 도와주는 똑똑한 가사 로봇이나 재난 구조 로봇을 만들어요.", "school": "서울로봇고, 수도전기공업고"},
        {"name": "스마트팜 운영 전문가", "desc": "IT 기술을 활용해 식물이 가장 잘 자라는 환경을 원격 제어해요.", "school": "수원농생명과학고, 한국바이오과학고"},
        {"name": "친환경 에너지 공학자", "desc": "지구를 살리기 위해 태양광, 수소 등 깨끗한 에너지를 연구해요.", "school": "한양공업고, 울산에너지고"}
    ]
}

# 3. 앱 상태 초기화 (Streamlit Session State)
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.selected_field = None
    st.session_state.game_jobs = []
    st.session_state.score = {}

st.title("🚀 내 미래를 Pick! 직업 밸런스 게임")
st.markdown("<div class='sub-title'>10번의 선택으로 알아보는 나의 취향 저격 미래 직업!</div>", unsafe_allow_html=True)

# Step 0: 대분류 분야 선택 탭 효과
if st.session_state.step == 0:
    st.info("💡 관심 있는 분야를 먼저 선택하면, 맞춤형 밸런스 게임이 시작됩니다!")
    fields = list(JOB_DATA.keys())
    
    # 아기자기한 버튼 배열
    cols = st.columns(len(fields))
    for i, field in enumerate(fields):
        with cols[i]:
            if st.button(field):
                st.session_state.selected_field = field
                # 해당 분야 및 전체에서 핫한 직업을 섞어 밸런스 게임 풀 구성
                pool = JOB_DATA[field] * 3  # 문제를 채우기 위해 셔플 풀 확보
                random.shuffle(pool)
                st.session_state.game_jobs = pool[:20] # 10단계를 위한 20개 직업 확보
                st.session_state.step = 1
                st.rerun()

# Step 1 ~ 10: 밸런스 게임 진행
elif 1 <= st.session_state.step <= 10:
    current_step = st.session_state.step
    
    # 귀여운 프로그레스 바 구현
    st.write(f"### 🎮 {current_step} / 10 단계 진행 중!")
    st.progress(current_step / 10)
    
    # 이번 단계에서 대결할 두 직업 매칭
    job_a = st.session_state.game_jobs[(current_step - 1) * 2]
    job_b = st.session_state.game_jobs[(current_step - 1) * 2 + 1]
    
    st.markdown("#### 🤔 둘 중 더 끌리고 재미있어 보이는 직업은?")
    
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

# Step 11: 최종 결과 및 특성화고/마이스터고 추천
else:
    st.balloons()
    st.success("🎉 10단계의 밸런스 게임을 모두 완료했습니다!")
    
    # 가장 많이 선택된 직업 추출
    if st.session_state.score:
        best_job_name = max(st.session_state.score, key=st.session_state.score.get)
    else:
        # 하나도 선택 안 된 예외 상황 방지
        best_job_name = st.session_state.game_jobs[0]['name']
        
    # 해당 직업의 정보 찾기
    final_job = None
    for field in JOB_DATA:
        for job in JOB_DATA[field]:
            if job['name'] == best_job_name:
                final_job = job
                break
                
    st.markdown(f"## 🏆 너의 미래 명함은: [{final_job['name']}]")
    st.subheader(f"✨ \"{final_job['desc']}\"")
    
    st.divider()
    
    # 관련 고등학교 정보 연계 추천
    st.markdown("### 🏫 이 직업을 꿈꿀 수 있는 추천 고등학교")
    st.info("해당 분야의 역량을 탄탄하게 키워주는 특성화고등학교 및 마이스터고등학교 리스트예요!")
    
    schools = final_job['school'].split(", ")
    for school in schools:
        st.markdown(f"* **{school}**")
        
    # 다시 하기 버튼
    if st.button("🔄 게임 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.selected_field = None
        st.session_state.game_jobs = []
        st.session_state.score = {}
        st.rerun()
