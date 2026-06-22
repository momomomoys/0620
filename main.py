import streamlit as st
import base64
from io import BytesIO

# --- [안전장치] gTTS 라이브러리 검증 및 서버 다운 방지 ---
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 음성 재생 함수 (속도를 조절해 발랄한 하이톤 유도) ---
def speak(text):
    if not gtts_available:
        return
    try:
        # 문장 부호를 활용해 자연스러운 억양 형성
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # HTML5 오디오 태그를 사용하여 끊김 현상과 브라우저 차단 완벽 우회
        audio_tag = f'<audio autoplay src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception:
        pass

# --- 디자인 스타일 설정 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght=400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Nanum Gothic', sans-serif; }
    
    .header-box {
        background-color: #96000F;
        padding: 35px;
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

# --- 부서별 데이터 리스트 ---
data = {
    "교무기획부": {
        "title": "🎨 나의 전공을 직접 디자인해!",
        "points": [
            "✨ 시각디자인과: 광고부터 UI 디자인까지 학년별 특화 과정!",
            "🎬 영상애니메이션과: 웹툰과 캐릭터, 애니메이션의 성지!",
            "🏫 내가 원하는 수업을 쏙쏙 골라 듣는 고교학점제 완벽 지원!"
        ],
        "voice": "안녕 친구들~! 교무기획부 홍이에요~! 우리 학교에서 너희의 꿈과 재능을 마음껏 펼칠 수 있는 멋진 수업들을 준비했어! 시각디자인이랑 영상애니메이션 중에 너는 어떤 과가 더 끌리니? 생각만 해도 너무 설레지 않아?",
        "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=600"
    },
    "교육연구부": {
        "title": "📚 지성과 감성을 한 번에!",
        "points": [
            "🖌️ 스토리텔링 일러스트 공모전 활동으로 나만의 삽화 그리기!",
            "📰 우리 손으로 소통하며 만드는 독서신문 '하루면가'!",
            "⭐ 포토샵, 일러스트 그래픽 자격증 취득 방과후 학교 전액 지원!"
        ],
        "voice": "책을 읽고 너만의 감
