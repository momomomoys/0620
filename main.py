import streamlit as st
import base64
from gtts import gTTS
import io

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 1. 음성 생성 함수 (여학생 목소리 느낌) ---
def speak(text):
    tts = gTTS(text=text, lang='ko')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio_bytes = fp.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    # HTML 오디오 태그를 사용하여 자동 재생 (사용자 클릭 없이 재생되도록 설정)
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)

# --- 2. 커스텀 CSS (학교 사진 활용 및 세련된 레이아웃) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&family=Nanum+Gothic:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #FFF5F7 0%, #FFFFFF 100%);
    }
    
    /* 상단 학교 사진 배경 스타일 */
    .header-box {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://raw.githubusercontent.com/user-attachments/assets/75a6c3f3-00e2-45e3-9828-090c29188e7c");
        background-size: cover;
        background-position: center;
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    /* 캐릭터 대화창 */
    .chat-bubble {
        background-color: white;
        border: 3px solid #FFB6C1;
        border-radius: 25px;
        padding: 25px;
        position: relative;
        font-family: 'Nanum Gothic', sans-serif;
        font-size: 20px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    
    .key-point {
        background-color: #96000F;
        color: white;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* 부서 버튼 스타일 */
    .stButton>button {
        background-color: white;
        border: 2px solid #96000F;
        color: #96000F;
        border-radius: 15px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #96000F;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 부서별 상세 데이터 ---
data = {
    "교무기획부": {
        "title": "내 전공을 디자인하다",
        "points": ["시각디자인과 3개 코스", "영상애니메이션과 2개 코스", "고교학점제 학생 선택권 강화"],
        "voice": "반가워 친구들! 교무기획부에서는 너희들의 꿈에 딱 맞는 전공 수업을 준비하고 있어. 어떤 전공이 너랑 어울릴지 같이 고민해볼까?",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/8f096283-7c85-48b4-9388-693240974b77" # 학교 실습실 사진 등
    },
    "진로교육부": {
        "title": "홍대 미대로 가는 지름길",
        "points": ["홍대 미대 진학 시 4년 전액 장학금", "매년 7~10% 홍대 진학률", "1:1 맞춤형 진로 컨설팅"],
        "voice": "와! 홍대 미대 가고 싶은 친구들 여기 보세요! 우리 학교는 홍대 병설이라 장학금 혜택이 어마어마해. 입학사정관님이 직접 오셔서 설명도 해주신단다!",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/75a6c3f3-00e2-45e3-9828-090c29188e7c"
    },
    "취업부": {
        "title": "글로벌 디자인 인재",
        "points": ["일본 오사카 글로벌 현장학습", "신한 커리어온 등 대기업 연계 교육", "자격증 응시료 전액 지원"],
        "voice": "세상은 넓고 할 일은 많다! 우리랑 같이 일본으로 디자인 연수 떠나지 않을래? 자격증 따는 비용도 학교에서 다 대줄게!",
        "image": "https://raw.githubusercontent.com/user-attachments/assets/8f096283-7c85-48b4-9388-693240974b77"
    },
    # 추가 부서들도 동일하게 작성...
}

# --- 4. 메인 화면 ---
st.markdown('<div class="header-box"><h1>🎨 홍익디자인고등학교 입학설명회</h1><p>내 꿈이 현실이 되는 곳, 홍디고에 오신 것을 환영합니다!</p></div>', unsafe_allow_html=True)

# 부서 선택 버튼 (상단 배치)
cols = st.columns(len(data))
selected_dept = st.session_state.get('dept', "진로교육부")

for i, dept_name in enumerate(data.keys()):
    if cols[i].button(dept_name):
        st.session_state.dept = dept_name
        selected_dept = dept_name
        # 버튼 누르면 바로 음성 재생
        speak(data[dept_name]["voice"])

st.divider()

# --- 5. 상세 내용 레이아웃 ---
col_char, col_content = st.columns([1, 1.5])

with col_char:
    # 교복 입은 캐릭터 이미지 (사용자가 제공한 이미지 URL 사용)
    st.image("https://raw.githubusercontent.com/user-attachments/assets/8d77c191-45da-4859-9946-993d05f3238d", use_container_width=True)
    st.markdown(f"""
        <div class="chat-bubble">
            <b>홍이:</b><br>
            "{data[selected_dept]['voice']}"
        </div>
    """, unsafe_allow_html=True)

with col_content:
    st.markdown(f"### 📍 {selected_dept}: {data[selected_dept]['title']}")
    
    # 키포인트 시각화
    for point in data[selected_dept]['points']:
        st.markdown(f'<div class="key-point">Key Point</div> {point}', unsafe_allow_html=True)
    
    st.write("")
    # 부서별 관련 사진
    st.image(data[selected_dept]['image'], caption=f"{selected_dept} 활동 모습", use_container_width=True)
    
    st.success(f"💡 선생님께서 **{selected_dept}**의 상세 활동에 대해 추가 설명을 해주시겠습니다.")

# --- 6. 푸터 및 정보 ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>본 웹앱은 홍익디자인고등학교 1차 입학설명회를 위해 제작되었습니다.</p>", unsafe_allow_html=True)
