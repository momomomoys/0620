import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
from io import BytesIO

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 음성 생성 및 자동 재생 함수 (TTS) ---
def speak(text, dept_name):
    tts = gTTS(text=text, lang='ko')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_base64 = base64.b64encode(fp.read()).decode()
    
    # 브라우저에서 버튼 클릭 시 음성이 즉시 자동 재생되도록 설정
    audio_tag = f'<audio autoplay="true" id="audio_{dept_name}" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)

# --- 커스텀 디자인 CSS (여학생 취향 저격 파스텔톤) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Nanum Gothic', sans-serif; }
    
    /* 상단 타이틀 영역 */
    .header-box {
        background-color: #96000F; /* 홍익대 상징색 레트로 레드 */
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 캐릭터 말풍선 */
    .chat-bubble {
        background-color: #FFF5F7;
        border: 3px solid #FBCFE8;
        border-radius: 25px;
        padding: 20px;
        margin-top: 15px;
        font-size: 18px;
        position: relative;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
    }
    
    /* 핵심 포인트 스타일 */
    .point-box {
        background-color: #FDF2F8;
        border-left: 5px solid #DB2777;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 4px 12px 12px 4px;
        font-size: 18px;
    }
    
    /* 상단 부서 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        border: 2px solid #FBCFE8;
        color: #DB2777;
        border-radius: 15px;
        font-weight: bold;
        font-size: 16px;
        height: 50px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #DB2777;
        color: white;
        border-color: #DB2777;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 학교 사진 및 부서별 데이터 (교무, 교육, 학생, 특성화, 진로, 취업) ---
data = {
    "교무기획부": {
        "points": ["🎨 시각디자인과 (광고, 편집, UI 디자인 코스)", "🎬 영상애니메이션과 (만화, 영상, 캐릭터, 애니메이터 코스)", "🏫 고교학점제 도입으로 나만의 맞춤형 시간표 디자인"],
        "voice": "안녕 친구들! 교무기획부에서는 너희의 소중한 전공 수업을 담당해. 시각디자인과 영상애니메이션과 중 너의 픽은 어디니?",
        "bg_img": "
