import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 디자인 스타일 설정 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght=400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Nanum Gothic', sans-serif; }
    
    .header-box {
        background-color: #96000F;
        padding: 40px;
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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFB6C1;
        color: white;
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

# --- 브라우저 내장 Web Speech API 음성 재생 스크립트 함수 ---
def play_browser_tts(text):
    # 외부 라이브러리 없이 브라우저 자체 여성 음성 엔진을 깨워 발랄한 톤(속도 1.1, 음높이 1.2)으로 스피킹합니다.
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            // 기존 재생 중인 음성 즉시 중단
            window.speechSynthesis.cancel();
            
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.lang = "ko-KR";
            msg.rate = 1.1;   // 약간 빠른 템포로 지루함 방지
            msg.pitch = 1.2;  // 음높이를 높여 귀여운 청소년/여학생 목소리 유도
            
            // 한국어 여성 음성 선호 설정
            var voices = window.speechSynthesis.getVoices();
            for(var i = 0; i < voices.length; i++) {{
                if(voices[i].lang === 'ko-KR' || voices[i].name.includes('Google 한국어') || voices[i].name.includes('Yuri')) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- 부서별 데이터 ---
data = {
    "교무기획부": {
        "title": "🎨 나의 전공을 직접 디자인해!",
        "points": [
            "✨ 시각디자인과: 광고부터 UI 디자인까지 학년별 특화 과정!",
            "🎬 영상애니메이션과: 웹툰과 캐릭터, 애니메이션의 성지!",
            "🏫 내가 원하는 수업을 쏙쏙 골라 듣는 고교학점제 완벽 지원!"
        ],
        "voice": "안녕 친구들~! 교무기획부 홍이에요~! 우리 학교에서 너희의 꿈과 재능을 마음껏 펼칠 수 있는 멋진 수업들을 준비했어! 시각디자인이랑 영상애니메이션 중에 너는 어떤 과가 더 끌리니? 생각만 해도 너무 설레지 않아?",
        "img": "
