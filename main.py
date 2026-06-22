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

# --- 귀여운 여학생 목소리 출력을 위한 안전한 자바스크립트 TTS 함수 ---
def play_female_tts(text):
    # 삼중 따옴표 내부에 안전하게 텍스트를 삽입하여 줄바꿈 에러를 방지합니다.
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = "ko-KR";
            msg.rate = 1.15;  
            msg.pitch = 1.35; 
            
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

# --- 부서별 데이터 (삼중 따옴표 처리로 문자열 끊김 완벽 방지) ---
data = {
    "교무기획부": {
        "title": """🎨 나의 전공을 직접 디자인해!""",
        "points": [
            """✨ 시각디자인과: 광고부터 UI 디자인까지 학년별 특화 과정!""",
            """🎬 영상애니메이션과: 웹툰과 캐릭터, 애니메이션의 성지!""",
