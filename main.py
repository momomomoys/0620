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

# --- 음성 재생 함수 (귀여운 여학생 톤 업그레이드) ---
def speak(text, dept_name):
    if not gtts_available:
        return
    try:
        # 밝고 귀여운 하이톤 유도를 위해 어미 수정 및 gTTS 호출
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # 💡 성인 남자 목소리처럼 처지는 것을 막기 위해 오디오 재생 속도(playbackRate)를 1.15배로 높여 
        # 한층 더 발랄하고 귀여운 여학생 목소리 톤을 강제로 만들어냅니다.
        audio_id = f"audio_{dept_name}"
        audio_tag = f"""
        <audio autoplay id="{audio_id}" src="data:audio/mp3;base64,{audio_base64}"></audio>
        <script>
            var audio = document.getElementById("{audio_id}");
            if (audio) {{
                audio.playbackRate = 1.15;
            }}
        </script>
        """
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

# --- 부서별 데이터 (말투 최적화) ---
data = {
    "교무기획부": {
