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
        "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600&auto=format&fit=crop"
    },
    "학생안전복지부": {
        "title": "🛍️ 동아리 활동이 제일 재밌어!",
        "points": [
            "창업 동아리 SPAM: 굿즈 제작부터 판매 마켓까지!",
            "바이오메디컬 아트: 메디컬 일러스트레이터 진로 탐구!",
            "총 40개의 힙한 동아리가 너희를 기다려!"
        ],
        "voice": "우리 학교 동아리 활동은 진짜 꿀잼이야! 친구들이랑 직접 굿즈를 만들어서 팔아보기도 하고, 신기한 메디컬 일러스트도 배울 수 있어. 학교 오는 게 매일 즐거울 거야~!",
        "img": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?q=80&w=600&auto=format&fit=crop"
    },
    "특성화정보부": {
        "title": "🤖 미래를 디자인하는 AI 기술!",
        "points": [
            "AI 미래 디자인 한마당: 생성형 AI 실무 활용!",
            "전국 상업경진대회 참가 적극 지원 및 특별 지도!",
            "프리미엄 실습실과 최신 어도비 소프트웨어 지원!"
        ],
        "voice": "미래의 디자이너라면 AI 정도는 다뤄야지? 미드저니 같은 인공지능으로 너희의 상상력을 더 넓혀봐! 최고 사양 컴퓨터랑 어도비 프로그램도 빵빵하게 지원해줄게!",
        "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop"
    },
    "진로교육부": {
        "title": "🎖️ 홍대 미대의 주인공은 너!",
        "points": [
            "본교 졸업생 홍대 미대 진학 시 4년 전액 장학금!",
            "매년 7~10% 홍대 미대 진학 (최근 6년간 50명!)",
            "입학사정관 초청 1:1 맞춤형 진로 컨설팅!"
        ],
        "voice": "와~! 대박 소식! 우리 학교 졸업하고 홍대 미대 가면 4년 동안 장학금을 준대! 홍대 미대 진학률 1위, 바로 우리 학교야! 홍대 가고 싶은 친구들 다 모여라~!",
        "img": "https://raw.githubusercontent.com/user-attachments/assets/75a6c3f3-00e2-45e3-9828-090c29188e7c"
    },
    "취업부": {
        "title": "✈️ 일본으로 디자인 연수 가자!",
        "points": [
            "글로벌 현장학습: 일본 오사카·교토 직무 연수!",
            "대기업 연계 직무 교육 및 취업 마스터 클래스!",
            "드림 성장 바우처 & 자격증 응시료 전액 지원!"
        ],
        "voice": "친구들, 일본 오사카랑 교토로 디자인 연수 가볼래? 전액 지원이라니 믿기지 않지? 취업부에서는 너희의 글로벌한 성장을 위해 모든 걸 지원해줄게. 진짜 최고야!",
        "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=600&auto=format&fit=crop"
    }
}

# --- 메인 화면 레이아웃 ---
st.markdown('<div class="header-box"><h1>🎨 홍익디자인고 입학설명회</h1><p style="font-size:18px;">꿈이 현실이 되는 곳, 홍이 세 자매가 안내해줄게!</p></div>', unsafe_allow_html=True)

# 부서 선택 버튼 (상단)
dept_names = list(data.keys())
cols = st.columns(len(dept_names))
selected_dept = st.session_state.get('dept', "교무기획부")

for i, dept_name in enumerate(dept_names):
    if cols[i].button(dept_name):
        st.session_state.dept = dept_name
        selected_dept = dept_name
        speak(data[dept_name]["voice"], dept_name)

st.divider()

# --- 캐릭터 전면 배치 레이아웃 ---
col_left, col_right = st.columns([1.1, 1])

with col_left:
    # 에러 여지가 있는 모든 부가 설정을 제거하고 원본 주소만 깔끔하게 호출
    st.image("https://raw.githubusercontent.com/user-attachments/assets/26d2e616-43f1-4823-bc97-885b597df388")

with col_right:
    # 캐릭터 말풍선
    st.markdown(f"""
        <div class="chat-bubble">
            <b>🎀 홍이 :</b><br>
            "{data[selected_dept]['voice']}"
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # 부서 정보 상세 요약
    st.markdown(f"### {data[selected_dept]['title']}")
    for pt in data[selected_dept]["points"]:
        st.markdown(f'<div class="point-card">{pt}</div>', unsafe_allow_html=True)
    
    # 오류를 유발했던 인자들을 완전히 수정한 안전한 부서 이미지 코드
    st.image(data[selected_dept]['img'])

# --- 푸터 ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 홍익디자인고등학교 입학설명회 홍보 웹앱</p>", unsafe_allow_html=True)
