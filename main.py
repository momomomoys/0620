import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# --- gTTS 라이브러리 설치 여부 체크 (에러 완벽 방지) ---
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
        # 문장 끝에 문장 부호와 이모티콘을 섞어 톤을 높인 귀여운 음성을 유도합니다.
        tts = gTTS(text=text, lang='ko')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_base64 = base64.b64encode(fp.read()).decode()
        
        # HTML5 자동재생 오디오 태그
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

# --- 부서별 데이터 ---
data = {
    "교무기획부": {
        "title": "🎨 나의 전공을 직접 디자인해!",
        "points": [
            "✨ 시각디자인과: 광고부터 UI 디자인까지 학년별 특화 과정!",
            "🎬 영상애니메이션과: 웹툰과 캐릭터, 애니메이션의 성지!",
            "🏫 내가 원하는 수업을 쏙쏙 골라 듣는 고교학점제 완벽 지원!"
        ],
        "voice": "안녕 친구들~! 교무기획부 홍이에요~! 우리 학교에서 너희의 꿈과 재능을 마음껏 펼칠 수 있는 멋진 수업들을 준비했어! 시각디자인이랑 영상애니메이션 중에 너는 어떤 과가 더 끌리니? 생각만 해도 너무 설레지 않아?",
        "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=600"
    },
    "교육연구부": {
        "title": "📚 지성과 감성을 한 번에!",
        "points": [
            "🖌️ 스토리텔링 일러스트 공모전 활동으로 나만의 삽화 그리기!",
            "📰 우리 손으로 소통하며 만드는 독서신문 '하루면가'!",
            "⭐ 포토샵, 일러스트 그래픽 자격증 취득 방과후 학교 전액 지원!"
        ],
        "voice": "책을 읽고 너만의 감성이 담긴 멋진 그림을 그려보는 건 어때? 교육연구부에서는 너희의 상상력을 듬뿍 담은 멋진 디자인 활동을 전폭 지원해! 자격증 공부도 전액 무료로 도와줄게, 우리 함께 도전해봐요~!",
        "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600"
    },
    "학생안전복지부": {
        "title": "🛍️ 동아리 활동, 여기가 찐이야!",
        "points": [
            "🔥 창업 동아리 SPAM: 내 손으로 굿즈를 기획·제작하고 직접 판매까지!",
            "🧬 바이오메디컬 아트: 미래 유망 진로 메디컬 일러스트 정밀 체험!",
            "🎈 무려 40개의 개성 넘치고 힙한 동아리가 너희를 기다려!"
        ],
        "voice": "우리 학교 동아리는 진짜 상상 초월 꿀잼 보장이야~! 친구들이랑 직접 예쁜 굿즈를 만들어서 마켓도 열고, 신기한 메디컬 아트도 전공할 수 있어! 매일매일 학교 오는 게 축제 같을 거야~!",
        "img": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?q=80&w=600"
    },
    "특성화정보부": {
        "title": "🤖 AI 기술로 앞서가는 크리에이터!",
        "points": [
            "🖥️ AI 미래 디자인 한마당: 생성형 AI 툴을 활용한 트렌디 디자인 실습!",
            "🏆 서울시 및 전국 상업경진대회 1:1 특별 지도와 참가 적극 지원!",
            "💎 최고 사양 프리미엄 PC 실습실 및 전교생 정품 어도비 소프트웨어 지원!"
        ],
        "voice": "트렌디한 디자이너라면 최신 AI 기술 정도는 다뤄줘야지~? 미드저니 같은 인공지능을 활용해서 너희의 상상력을 우주 끝까지 펼쳐봐! 최고 사양 컴퓨터와 최신 프로그램도 마음껏 지원해줄게!",
        "img": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600"
    },
    "진로교육부": {
        "title": "🎖️ 꿈의 홍대 미대, 현실이 된다!",
        "points": [
            "🎁 本校 졸업생이 홍익대학교 미술대학 진학 시 4년 전액 장학금 파격 혜택!",
            "📈 매년 고교 전체 졸업생 중 7~10% 수준의 독보적인 홍대 진학률!",
            "🎯 입학사정관 초청 1:1 맞춤형 수시 학생부 종합 전형 진로 컨설팅!"
        ],
        "voice": "얘들아, 진짜 엄청난 소식 알려줄까? 우리 학교를 졸업하고 꿈의 홍대 미대에 가면 4년 내내 등록금 전액을 장학금으로 준대! 홍대 미대 진학률 최고를 자랑하는 우리 학교에서 너도 주인공이 되어봐!",
        "img": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=600"
    },
    "취업부": {
        "title": "✈️ 일본으로 디자인 글로벌 연수 떠나자!",
        "points": [
            "🇯🇵 글로벌 현장학습: 일본 오사카와 교토 무료 직무 연수 및 문화 탐방!",
            "💼 대기업 연계 직무 교육 및 넷마블, 신한 커리어온 매칭 취업 캠프!",
            "💰 드림 성장 바우처
