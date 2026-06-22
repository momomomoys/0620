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

# --- 3. 💡 [중요] 귀여운 여학생 목소리 자바스크립트 함수 ---
def play_female_voice(text):
    # 음높이(pitch)를 1.4로 높여서 귀여운 소녀 톤을 만듭니다.
    js_code = f"""
    <script>
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = "ko-KR";
            msg.rate = 1.1;   // 약간 빠른 속도
            msg.pitch = 1.4;  // 고음 (여학생 느낌)
            
            var voices = window.speechSynthesis.getVoices();
            // 가장 부드러운 여성 목소리 찾기
            var selectedVoice = voices.find(v => v.name.includes('Google 한국어') || v.name.includes('Yuri') || v.name.includes('Heami'));
            if(selectedVoice) msg.voice = selectedVoice;
            
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# --- 4. 부서별 데이터 (삼중 따옴표로 에러 방지) ---
data = {
    "교무기획부": {
        "title": """🎨 나의 전공을 직접 디자인해!""",
        "points": ["""
