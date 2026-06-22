import streamlit as st
import pandas as pd
from gtts import gTTS
import base64
import os
import requests
from io import BytesIO

# --- 설정 (필수!) ---
# OpenAI API Key: "본인의 실제 OpenAI API Key"를 입력하세요.
# 만약 깃허브에 공유할 예정이라면 절대 여기에 키를 쓰지 말고, 
# .streamlit/secrets.toml 파일을 만들어 관리해야 합니다.
# 예시: openai_key = st.secrets["OPENAI_KEY"]
openai_key = "YOUR_OPENAI_API_KEY_HERE" 

# --- 캐릭터 생성 함수 (DALL-E) ---
@st.cache_resource() # 이미지 생성은 비용이 드니 결과물을 캐싱합니다.
def generate_character_image(key):
    if key == "YOUR_OPENAI_API_KEY_HERE":
        st.error("OpenAI API Key가 설정되지 않았습니다. 코드를 수정해주세요.")
        return None

    # 중3 여학생들의 취향을 고려한 3D 캐릭터 스타일 프롬프트
    prompt = """
    A cute 3D character illustration of a smiling Korean high school girl. 
    She is wearing a stylish, neat dark navy blue school uniform with a white blouse, a red tie, and a gray plait skirt. 
    She has short dark brown hair with straight bangs. 
    She is in a modern, brightly lit interior of an art school hallway. 
    The style is friendly, similar to an animation studio character design. 
    Full body shot, centered, clear white background.
    """
    
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        image_url = response_data['data'][0]['url']
        
        # 이미지 다운로드
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            return BytesIO(img_response.content)
        else:
            st.error("캐릭터 이미지를 다운로드하는 데 실패했습니다.")
            return None
            
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
        return None

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 캐릭터 생성 및 로드 ---
if 'char_image_data' not in st.session_state:
    with st.spinner("우리 학교 홍보 캐릭터를 디자인하는 중이에요... 잠시만 기다려줘!"):
        st.session_state.char_image_data = generate_character_image(openai_key)

# --- 1. 음성 생성 함수 (TTS) ---
def speak(text, dept_name):
    tts = gTTS(text=text, lang='ko')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_bytes = fp.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # 각 부서별로 고유한 오디오 태그 아이디를 부여하여 재생 제어
    audio_tag = f'<audio autoplay="true" id="audio_{dept_name}" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)

# --- 2. 커스텀 CSS (세련된 스타일링) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Nanum+Gothic:wght@400;700&display=swap');
    
    .main {
        background-color: #FFFFFF;
    }
    
    h1, h2, h3, h4, p, stButton {
        font-family: 'Nanum Gothic', sans-serif;
    }

    /* 상단 학교 사진 배경 스타일 */
    .header-box {
        background-color: #96000F; /* 홍익대 상징색 */
        background-image: linear-gradient(rgba(150, 0, 15, 0.8), rgba(150, 0, 15, 0.9)), url("https://raw.githubusercontent.com/user-attachments/assets/75a6c3f3-00e2-45e3-9828-090c29188e7c");
        background-size: cover;
        background-position: center;
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    /* 캐릭터 대화창 */
    .chat-bubble {
        background-color: white;
        border: 3px solid #fdd5bd;
        border-radius: 25px;
        padding: 20px;
        margin-top: 15px;
        font-size: 18px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    
    .key-point-title {
        color: #96000F;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    /* 부서 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background-color: #fdf2f8;
        border: 2px solid #fce7f3;
        color: #db2777;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #db2777;
        border-color: #db2777;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 부서별 데이터 ---
data = {
    "교무기획부": {
        "points": ["학과별 특화 교육과정 (시각/영상)", "학생 맞춤형 고교학점제", "창의 융합 디자인 수업"],
        "voice": "반가워! 교무기획부에서는 너의 꿈에 맞춘 전공 수업을 디자인해준단다! 같이 크리에이티브하게 놀아보자!",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/8f096283-7c85-48b4-9388-693240974b77"
    },
    "진로교육부": {
        "points": ["홍대 미대 4년 전액 장학금 (본교졸업생)", "매년 7~10% 홍대 미대 진학", "전문 진학 컨설팅 및 멘토링"],
        "voice": "홍대 미대 가고 싶은 친구? 우리 학교에선 그 꿈, 현실로 만들 수 있어! 장학금까지 빵빵하게 줄게!",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/75a6c3f3-00e2-45e3-9828-090c29188e7c"
    },
    "취업부": {
        "points": ["글로벌 현장학습 (일본)", "대기업 연계 직무 교육", "자격증 취득 및 포트폴리오 지원"],
        "voice": "디자이너로 해외 가고 싶다고? 일본 현장학습, 취업부가 다~ 준비했어! 자격증 따는 돈도 학교가 낸다!",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/8f096283-7c85-48b4-9388-693240974b77"
    },
}

# --- 4. 메인 화면 ---
st.markdown('<div class="header-box"><h1>🎨 홍익디자인고등학교 입학설명회</h1><p>내 꿈을 디자인하는 첫걸음, 홍이와 함께해요!</p></div>', unsafe_allow_html=True)

# 부서 선택 버튼 (상단)
dept_names = list(data.keys())
cols = st.columns(len(dept_names))

# 세션 상태로 현재 선택된 부서 관리
selected_dept = st.session_state.get('dept', "진로교육부")

for i, dept_name in enumerate(dept_names):
    if cols[i].button(dept_name):
        st.session_state.dept = dept_name
        selected_dept = dept_name
        # 버튼 누를 때마다 TTS 재생
        speak(data[dept_name]["voice"], dept_name)

st.divider()

# --- 5. 콘텐츠 레이아웃 (캐릭터 | 내용) ---
col_char, col_content = st.columns([1, 1.3])

with col_char:
    # 생성된 캐릭터 이미지 표시
    if st.session_state.char_image_data:
        st.image(st.session_state.char_image_data, use_container_width=True)
        st.markdown(f'<div class="chat-bubble"><b>홍이:</b> "{data[selected_dept]["voice"]}"</div>', unsafe_allow_html=True)
    else:
        st.warning("캐릭터 이미지를 생성하지 못했습니다. API Key를 확인해주세요.")

with col_content:
    st.markdown(f"### 📍 {selected_dept}")
    
    st.image(data[selected_dept]['image'], caption=f"{selected_dept} 주요 활동", use_container_width=True)

    st.markdown("<br><h4>⭐ 핵심 포인트</h4>", unsafe_allow_html=True)
    # 키포인트 시각화
    for point in data[selected_dept]['points']:
        st.markdown(f'<p><span class="key-point-title">•</span> {point}</p>', unsafe_allow_html=True)
    
    st.info(f"💡 선생님께서 **{selected_dept}**에 대해 더 자세히 설명해주시겠습니다.")

# --- 6. 푸터 ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 홍익디자인고등학교 입학홍보팀</p>", unsafe_allow_html=True)
