import streamlit as st
import os

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 디자인 스타일 설정 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght=400;700&display=swap');
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

# --- 💡 [강화버전] 귀여운 여학생 목소리 자바스크립트 함수 ---
def play_female_tts(text):
    # 자바스크립트 내에서 텍스트가 깨지지 않도록 백틱(`)을 사용하고, 브라우저 음성 엔진을 즉시 깨우는 로직을 추가했습니다.
    js_code = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                // 1. 기존에 재생 중이던 음성이 있다면 즉시 취소
                window.speechSynthesis.cancel();
                
                // 2. 새로운 음성 객체 생성
                var msg = new SpeechSynthesisUtterance(`{text}`);
                msg.lang = "ko-KR";
                msg.rate = 1.15;  // 통통 튀는 약간 빠른 속도
                msg.pitch = 1.40; // 음높이를 높여 귀여운 여학생 톤으로 설정
                
                // 3. 브라우저가 가진 목소리 목록 검색 및 여성 목소리 매칭 보완
                var voices = window.speechSynthesis.getVoices();
                if(voices.length > 0) {{
                    for(var i = 0; i < voices.length; i++) {{
                        if(voices[i].lang === 'ko-KR' && (voices[i].name.includes('Google') || voices[i].name.includes('Yuri') || voices[i].name.includes('Heami'))) {{
                            msg.voice = voices[i];
                            break;
                        }}
                    }}
                }}
                
                # 4. 즉시 말하기 실행
                window.speechSynthesis.speak(msg);
            }}
        }})();
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- 부서별 데이터 ---
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

# --- 상단 타이틀 ---
st.markdown("""<div class="header-box"><h1>🎨 홍익디자인고 입학설명회</h1><p style="font-size:18px;">나를 가장 멋지게 디자인하는 공간, 홍이 세 자매가 안내할게!</p></div>""", unsafe_allow_html=True)

# 부서 선택 버튼
dept_names = list(data.keys())
cols = st.columns(len(dept_names))

# 세션 상태 초기화 및 현재 선택된 부서 가져오기
if 'dept' not in st.session_state:
    st.session_state.dept = "교무기획부"
