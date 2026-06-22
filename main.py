import streamlit as st
import os

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 2. 디자인 스타일 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Nanum Gothic', sans-serif; }
    
    .header-box {
        background-color: #96000F;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    
    .chat-bubble {
        background-color: #FFFFFF;
        border: 4px solid #FFB6C1;
        border-radius: 30px;
        padding: 25px;
        margin-top: 10px;
        font-size: 20px;
        line-height: 1.6;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        position: relative;
    }

    .chat-bubble::after {
        content: '';
        position: absolute;
        top: 40%;
        left: -20px;
        border-width: 10px 20px 10px 0;
        border-style: solid;
        border-color: transparent #FFB6C1 transparent transparent;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        border: 2px solid #FFB6C1;
        color: #DB2777;
        border-radius: 15px;
        font-weight: bold;
        height: 55px;
        font-size: 16px;
    }

    .point-card {
        background-color: #FFF5F7;
        border-left: 6px solid #FF69B4;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 귀여운 여학생 목소리 자바스크립트 함수 ---
def play_female_voice(text):
    # 자바스크립트 내에서 줄바꿈이나 기호로 인해 깨지지 않도록 백틱(``) 처리를 확실히 했습니다.
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = "ko-KR";
            msg.rate = 1.1;   
            msg.pitch = 1.4;  
            
            var voices = window.speechSynthesis.getVoices();
            var selectedVoice = voices.find(v => v.name.includes('Google 한국어') || v.name.includes('Yuri') || v.name.includes('Heami'));
            if(selectedVoice) msg.voice = selectedVoice;
            
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- 4. 부서별 데이터 (따옴표 에러가 없도록 한 줄로 깔끔하게 정리) ---
data = {
    "교무기획부": {
        "title": "🎨 나의 전공을 직접 디자인해!",
        "points": ["✨ 시각디자인과: 광고부터 UI 디자인까지 특화 과정!", "🎬 영상애니메이션과: 웹툰과 캐릭터 애니메이션의 성지!", "🏫 수업을 골라 듣는 고교학점제 완벽 지원!"],
        "voice": "안녕 친구들~! 교무기획부 홍이에요~! 우리 학교에서 너희의 꿈과 재능을 마음껏 펼칠 수 있는 멋진 수업들을 준비했어! 시각디자인이랑 영상애니메이션 중에 어떤 과가 더 끌리니?",
        "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=600"
    },
    "교육연구부": {
        "title": "📚 지성과 감성을 한 번에!",
        "points": ["🖌️ 스토리텔링 일러스트 공모전 활동 지원!", "📰 우리 손으로 만드는 독서신문 '하루면가'!", "⭐ 포토샵, 일러스트 그래픽 자격증 취득 전액 지원!"],
        "voice": "책을 읽고 너만의 감성이 담긴 멋진 그림을 그려보는 건 어때? 교육연구부에서는 너희의 상상력을 듬뿍 담은 멋진 디자인 활동을 전폭 지원해! 우리 함께 도전해봐요~!",
        "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600"
    },
    "학생안전복지부": {
        "title": "🛍️ 동아리 활동, 여기가 찐이야!",
        "points": ["🔥 창업 동아리 SPAM: 내 손으로 굿즈를 기획 및 직접 판매!", "🧬 바이오메디컬 아트: 미래 유망 진로 일러스트 체험!", "🎈 무려 40개의 개성 넘치고 힙한 동아리가 대기 중!"],
        "voice": "우리 학교 동아리는 진짜 상상 초월 꿀잼 보장이야~! 친구들이랑 직접 예쁜 굿즈를 만들어서 마켓도 열고, 신기한 메디컬 아트도 전공할 수 있어! 매일 학교 오는 게 축제 같을 거야!",
        "img": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?q=80&w=600"
    },
    "특성화정보부": {
        "title": "🤖 AI 기술로 앞서가는 크리에이터!",
        "points": ["🖥️ AI 미래 디자인 한마당: 생성형 AI 툴 디자인 실습!", "🏆 서울시 및 전국 상업경진대회 1:1 특별 지도 지원!", "💎 최고 사양 프리미엄 PC 및 전교생 정품 어도비 지원!"],
        "voice": "트렌디한 디자이너라면 최신 AI 기술 정도는 다뤄줘야지~? 인공지능을 활용해서 너희의 상상력을 우주 끝까지 펼쳐봐! 최고 사양 컴퓨터와 최신 프로그램도 마음껏 지원해줄게!",
        "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600"
    },
    "진로교육부": {
        "title": "🎖️ 꿈의 홍대 미대, 현실이 된다!",
        "points": ["🎁 홍익대학교 미술대학 진학 시 4년 전액 장학금 혜택!", "📈 매년 독보적인 홍대 진학률 자랑!", "🎯 입학사정관 초청 1:1 맞춤형 수시 진로 컨설팅!"],
        "voice": "얘들아, 진짜 엄청난 소식 알려줄까? 우리 학교를 졸업하고 꿈의 홍대 미대에 가면 4년 내내 등록금 전액을 장학금으로 준대! 홍대 미대 진학률 최고를 자랑하는 우리 학교에서 너도 주인공이 되어봐!",
        "img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    "취업부": {
        "title": "✈️ 일본으로 디자인 글로벌 연수 떠나자!",
        "points": ["🇯🇵 글로벌 현장학습: 일본 오사카와 교토 무료 직무 연수!", "💼 넷마블, 신한 커리어온 매칭 취업 캠프!", "💰 드림 성장 바우처 및 자격증 응시 수수료 100% 지원!"],
        "voice": "친구들~! 고등학교 다니면서 일본으로 무상 디자인 연수 떠나보고 싶지 않아? 일본 오사카와 교토로 향하는 현장 학습이 널 기다려! 취업 준비 비용은 학교가 전부 책임질게, 진짜 최고지?",
        "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=600"
    }
}

# --- 5. 상단 타이틀 ---
st.markdown("""<div class="header-box"><h1>🎨 홍익디자인고 입학설명회</h1><p style="font-size:18px;">나를 가장 멋지게 디자인하는 공간, 홍이 세 자매가 안내할게!</p></div>""", unsafe_allow_html=True)

# --- 6. 부서 선택 버튼 ---
dept_names = list(data.keys())
cols = st.columns(len(dept_names))

if 'dept' not in st.session_state:
    st.session_state.dept = "교무기획부"

for i, dept_name in enumerate(dept_names):
    if cols[i].button(dept_name):
        st.session_state.dept = dept_name
        # 버튼을 누를 때 목소리 함수 실행
        play_female_voice(data[dept_name]["voice"])

selected_dept = st.session_state.dept

st.divider()

# --- 7. 메인 레이아웃 (좌: 캐릭터 | 우: 설명 내용) ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
    image_path = "image.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("⚠️ 'image.jpg' 파일을 찾을 수 없습니다. GitHub에 사진이 잘 올라갔는지 확인해 주세요!")

with col_right:
    # 캐릭터 말풍선 대사창
    st.markdown(f"""
        <div class="chat-bubble">
            <b>🎀 홍이 :</b><br>
            "{data[selected_dept]['voice']}"
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # 세부 정보 카드 출력
    st.markdown(f"### {data[selected_dept]['title']}")
    for pt in data[selected_dept]["points"]:
        st.markdown(f'<div class="point-card">{pt}</div>', unsafe_allow_html=True)
    
    # 부서별 서브 이미지
    st.image(data[selected_dept]['img'], use_container_width=True)

# --- 8. 푸터 ---
st.markdown("---")
st.markdown("""<p style='text-align: center; color: #94A3B8;'>© 2026 홍익디자인고등학교 입학설명회 시스템</p>""", unsafe_allow_html=True)
