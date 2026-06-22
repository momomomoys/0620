import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# --- gTTS 라이브러리 설치 여부 체크 ---
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 음성 재생 함수 ---
def speak(text, dept_name):
    if not gtts_available:
        return
    try:
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # 표준 HTML5 자동재생 오디오 태그
        audio_tag = f'<audio autoplay id="audio_{dept_name}" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception:
        pass

# --- 디자인 스타일 설정 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
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
        top: 50%;
        left: -20px;
        border-width: 10px 20px 10px 0;
        border-style: solid;
        border-color: transparent #FFB6C1 transparent transparent;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        border: 2px solid #96000F;
        color: #96000F;
        border-radius: 12px;
        font-weight: bold;
        height: 55px;
        font-size: 17px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #96000F;
        color: white;
    }

    .point-card {
        background-color: #FFF5F7;
        border-left: 6px solid #FF69B4;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 부서별 데이터 ---
data = {
    "교무기획부": {
        "title": "🎨 너의 전공을 디자인해봐!",
        "points": [
            "시각디자인과: 광고, 편집, UI 디자인 전문가 과정!",
            "영상애니메이션과: 웹툰, 영상, 캐릭터 디자인의 성지!",
            "원하는 수업을 골라 듣는 고교학점제까지 완벽해!"
        ],
        "voice": "안녕 친구들~! 교무기획부에서는 너희의 재능을 꽃피울 멋진 수업들을 준비하고 있어! 시각디자인이랑 영상애니메이션 중에서 너는 어떤 걸 배우고 싶니? 너무 설레지 않아?",
        "img": "https://raw.githubusercontent.com/user-attachments/assets/8f096283-7c85-48b4-9388-693240974b77"
    },
    "교육연구부": {
        "title": "📚 지성과 감성의 하모니!",
        "points": [
            "스토리텔링 일러스트 활동으로 나만의 삽화 그리기!",
            "독서신문 '하루면가' 제작으로 디자인 역량 쑥쑥!",
            "자격증 취득반 방과후 수업 전액 지원 (GTQ 등)"
        ],
        "voice": "책을 읽고 나만의 멋진 그림을 그려보는 건 어때? 교육연구부에서는 너희의 인문학적 감성과 디자인 실력을 합쳐줄게! 자격증 공부도 학교에서 도와줄게, 화이팅~!",
        "img": "https://images.unsplash.
