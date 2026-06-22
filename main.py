import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# --- gTTS 라이브러리 설치 여부 안전하게 체크 ---
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

# --- 페이지 설정 ---
st.set_page_config(page_title="홍익디자인고 입학설명회", layout="wide")

# --- 음성 생성 및 자동 재생 함수 (TTS) ---
def speak(text, dept_name):
    if not gtts_available:
        # 라이브러리가 없을 때는 음성 재생을 건너뛰고 안내만 표시 (에러 방지)
        return
    
    try:
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # 브라우저에서 음성이 즉시 자동 재생되도록 설정
        audio_tag = f'<audio autoplay="true" id="audio_{dept_name}" src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception as e:
        pass

# --- 커스텀 디자인 CSS ---
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
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
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
    
    .point-box {
        background-color: #FDF2F8;
        border-left: 5px solid #DB2777;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 4px 12px 12px 4px;
        font-size: 18px;
    }
    
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

# --- 부서별 데이터 ---
data = {
    "교무기획부": {
        "points": ["🎨 시각디자인과 (광고, 편집, UI 디자인 코스)", "🎬 영상애니메이션과 (만화, 영상, 캐릭터, 애니메이터 코스)", "🏫 고교학점제 도입으로 나만의 맞춤형 시간표 디자인"],
        "voice": "안녕 친구들! 교무기획부에서는 너희의 소중한 전공 수업을 담당해. 시각디자인과 영상애니메이션과 중 너의 픽은 어디니?",
        "bg_img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=600&auto=format&fit=crop"
    },
    "교육연구부": {
        "points": ["📚 스토리텔링 일러스트 공모전 (인문학적 소양과 실기 융합)", "📰 전교생이 직접 만드는 독서신문 '하루면가' 발행", "✍️ GTQ 포토샵/일러스트 자격증 취득 방과후 학교 전액 지원"],
        "voice": "책을 읽고 나만의 삽화를 그리는 멋진 상상, 교육연구부와 함께라면 현실이 될 수 있어!",
        "bg_img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600&auto=format&fit=crop"
    },
    "학생안전복지부": {
        "points": ["🛍️ 창업 동아리 SPAM (굿즈 기획부터 제작, 실제 판매 마켓까지 경험)", "🧬 바이오메디컬 아트 (홍익대 교수 연계 메디컬 일러스트레이터 진로 개척)", "🎈 총 40개의 정규 및 자율 동아리로 지루할 틈 없는 학교 생활"],
        "voice": "우리 학교 동아리는 클래스가 달라! 축제와 마켓, 너희가 하고 싶은 동아리를 마음껏 펼쳐봐!",
        "bg_img": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?q=80&w=600&auto=format&fit=crop"
    },
    "특성화정보부": {
        "points": ["🤖 AI 미래 디자인 한마당 (Midjourney 등 생성형 AI를 활용한 실무)", "🏆 서울시 및 전국 상업경진대회 참가 대폭 지원", "💻 최고 사양 프리미엄 PC 실습실 및 정품 어도비 소프트웨어 제공"],
        "voice": "미래의 디자이너는 AI도 잘 다뤄야겠지? 특성화정보부에서 최첨단 기술과 디자인의 융합을 배워봐!",
        "bg_img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop"
    },
    "진로교육부": {
        "points": ["🎖️ 본교 졸업생이 홍익대학교 미술대학 진학 시 '4년 전액 장학금' 파격 지원", "📈 매년 전체 고교생 중 7~10% 수준의 압도적인 홍대 미대 합격률 기록", "🎯 서울시 교육청 진학 전문가 초청 1:1 맞춤형 수시 컨설팅"],
        "voice": "꿈의 대학 홍대 미대! 우리 학교가 가장 잘 보낸다는 사실 알고 있니? 4년 전액 장학금의 주인공이 되어봐!",
        "bg_img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600&auto=format&fit=crop"
    },
    "취업부": {
        "points": ["✈️ 글로벌 현장학습 (일본 오사카·교토 디자인 직무 연수 및 문화 체험)", "🤝 넷마블 직무 교육 및 신한 커리어온 등 대기업 연계 취업 마스터 클래스", "💳 드림 성장 바우처 지급 및 국가 공인 자격증 응시 수수료 전액 지원"],
        "voice": "고등학교 때 일본으로 전액 지원 디자인 연수를 간다고? 맞아! 취업부에서는 너의 글로벌 무대를 지원해!",
        "bg_img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=600&auto=format&fit=crop"
    }
}

# --- 메인 헤더 타이틀 ---
st.markdown('<div class="header-box"><h1>🎨 홍익디자인고등학교 입학설명회</h1><p style="font-size:18px;">내 꿈이 디자인되는 곳, 홍이와 함께 부서별 매력을 알아봐요!</p></div>', unsafe_allow_html=True)

# 라이브러리 미설치 시 경고 메시지 대신 친절한 안내 제공 (로컬 테스트용)
if not gtts_available:
    st.info("ℹ️ 현재 음성 기능(gTTS)이 준비 중입니다. 웹앱 화면은 정상 이용이 가능합니다.")

# 부서 선택 버튼 레이아웃
dept_names = list(data.keys())
cols = st.columns(len(dept_names))

selected_dept = st.session_state.get('dept', "교무기획부")

for i, dept_name in enumerate(dept_names):
    if cols[i].button(dept_name):
        st.session_state.dept = dept_name
        selected_dept = dept_name
        speak(data[dept_name]["voice"], dept_name)

st.divider()

# --- 콘텐츠 레이아웃 ---
col_left, col_right = st.columns([1, 1.4])

with col_left:
    st.image("https://images.unsplash.com/photo-1594744803329-e58b31de215f?q=80&w=600&auto=format&fit=crop", 
             caption="홍익디자인고 홍보요정 홍이", use_container_width=True)
    
    st.markdown(f"""
        <div class="chat-bubble">
            <b>🎀 홍이 :</b><br>
            "{data[selected_dept]['voice']}"
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"### 🏢 {selected_dept} 주요 지원 활동")
    
    for pt in data[selected_dept]["points"]:
        st.markdown(f'<div class="point-box">{pt}</div>', unsafe_allow_html=True)
        
    st.write("")
    st.image(data[selected_dept]['bg_img'], use_container_width=True)
    
    st.warning(f"🗣️ 선생님 가이드: 지금 화면에 띄워진 **{selected_dept}**의 핵심 지원 내용을 바탕으로 상세 멘트를 이어가시면 됩니다.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 홍익디자인고등학교 입학홍보팀</p>", unsafe_allow_html=True)
