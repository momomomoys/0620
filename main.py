import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# --- gTTS 라이브러리 체크 ---
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 음성 재생 함수 (발랄한 여학생 톤 최적화) ---
def speak(text, dept_name):
    if not gtts_available:
        return
    try:
        # 목소리가 성인 남자처럼 들리는 것을 방지하기 위해 
        # 문장 끝에 '!'나 '~'를 넣어 톤을 높이고, gTTS의 표준 여성 음성을 사용합니다.
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # HTML 오디오 태그 (자동재생)
        # 소리가 너무 낮게 깔리지 않도록 텍스트 구성을 발랄하게 수정했습니다.
        audio_tag = f'<audio autoplay id="audio_{dept_name}" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception:
        pass

# --- 디자인 스타일 설정 (여학생 취향 저격 핑크 & 레드) ---
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

    /* 말풍선 꼬리 */
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

# --- 부서별 데이터 (말투를 극도로 발랄하게 수정) ---
data = {
    "교무기획부": {
        "title": "🎨 나의 전공을 직접 디자인해!",
        "points": [
            "✨ 시각디자인과: 광고부터 UI 디자인까지!",
            "🎬 영상애니메이션과: 웹툰과 애니의 성지!",
            "🏫 내가 직접 짜는 시간표, 고교학점제!"
        ],
        "voice": "안녕 친구들~! 교무기획부 홍이에요~! 우리 학교에서 너희의 재능을 마음껏 펼칠 수 있는 수업들을 준비했어! 시각디
