import streamlit as st
from openai import OpenAI
import time
from datetime import datetime
import random
from typing import Dict, List
import json
import os

st.set_page_config(
    page_title="한국 현대 문학 창작 스튜디오",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OpenAI API 키 환경변수 처리 방식 수정
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.error("OpenAI API 키가 설정되지 않았습니다.")
    st.stop()

questions = {
    "서정": {
        "icon": "🌸",
        "description": "감정과 정서를 노래하는 시 창작",
        "questions": [
            "어떤 감정이나 정서를 표현하고 싶나요?",
            "시의 주제는 무엇인가요? (예: 사랑, 자연, 삶과 죽음)",
            "어떤 이미지나 비유를 사용하고 싶나요?",
            "시의 형식은 어떤 것을 선호하나요? (자유시, 정형시)",
            "어떤 분위기를 만들고 싶나요? (서정적, 우울한, 역동적 등)"
        ]
    },
    "서사": {
        "icon": "📖",
        "description": "이야기를 풀어내는 소설 창작",
        "questions": [
            "이야기의 주요 플롯은 무엇인가요?",
            "주인공의 성격을 어떻게 설정하고 싶나요?",
            "작품의 시대적 배경은 언제인가요?",
            "어떤 문체를 사용하고 싶나요? (1인칭, 3인칭 등)",
            "작품에서 다루고 싶은 주요 주제나 메시지가 있나요?"
        ]
    },
    "극": {
        "icon": "🎭",
        "description": "무대 위에서 펼쳐지는 희곡 창작",
        "questions": [
            "극의 주요 갈등은 무엇인가요?",
            "주요 등장인물들을 어떻게 설정하고 싶나요?",
            "극의 배경 (시간과 장소)은 어디인가요?",
            "어떤 종류의 극을 쓰고 싶나요? (비극, 희극, 풍자극 등)",
            "관객에게 전달하고 싶은 메시지는 무엇인가요?"
        ]
    },
    "교술": {
        "icon": "✍️",
        "description": "지식과 사상을 전달하는 글쓰기",
        "questions": [
            "어떤 주제나 개념을 설명하고 싶나요?",
            "목표로 하는 독자층은 누구인가요?",
            "어떤 형식을 사용하고 싶나요? (에세이, 논문, 평론 등)",
            "주장을 뒷받침할 주요 논거나 예시가 있나요?",
            "글의 톤은 어떻게 설정하고 싶나요? (학술적, 대중적, 비판적 등)"
        ]
    }
}

if 'works_history' not in st.session_state:
    st.session_state.works_history = []

if 'current_work' not in st.session_state:
    st.session_state.current_work = None

if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}

if 'show_generated_work' not in st.session_state:
    st.session_state.show_generated_work = False

@st.cache_data
def generate_work(genre: str, answers: List[str], style: str = "현대적", length: str = "중편") -> str:
    genre_prompts = {
        "서정": "감성적이고 은유적인 표현을 사용하여 시적 언어로",
        "서사": "생동감 있는 묘사와 입체적인 인물 설정으로",
        "극": "대사와 지시문을 포함한 희곡 형식으로",
        "교술": "논리적이고 설득력 있는 구조로"
    }
    
    prompt = f"""
    다음 정보를 바탕으로 한국 현대 문학의 {genre} 갈래에 해당하는 작품을 작성해주세요:

    1. {questions[genre]["questions"][0]}: {answers[0]}
    2. {questions[genre]["questions"][1]}: {answers[1]}
    3. {questions[genre]["questions"][2]}: {answers[2]}
    4. {questions[genre]["questions"][3]}: {answers[3]}
    5. {questions[genre]["questions"][4]}: {answers[4]}

    작품 스타일: {style}
    작품 길이: {length}

    {genre_prompts[genre]} 작성해주세요.
    한국 현대 문학의 특징과 {genre} 갈래의 특성을 잘 반영하고,
    독창적이면서도 문학적 가치가 있는 작품을 만들어주세요.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"당신은 한국 현대 문학의 {genre} 갈래에 정통한 작가입니다. 문학적 깊이와 예술성을 갖춘 작품을 창작해주세요."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=2000
    )

    return response.choices[0].message.content

@st.cache_data
def analyze_work(work_text: str, genre: str) -> str:
    prompt = f"""
    다음 {genre} 작품을 분석해주세요:

    {work_text}

    다음 측면에서 간단히 분석해주세요:
    1. 문학적 기법과 특징
    2. 주제 의식
    3. 장점과 개선점
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 문학 평론가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

@st.cache_data
def get_writing_prompt(genre: str) -> str:
    prompts = {
        "서정": [
            "봄날의 첫사랑에 대한 시를 써보세요",
            "고향을 떠난 마음을 노래해보세요",
            "비 오는 날의 감성을 표현해보세요",
            "새벽의 고요함을 노래해보세요",
            "시간의 흐름에 대한 사색을 담아보세요"
        ],
        "서사": [
            "평범한 일상 속 특별한 하루",
            "잃어버린 물건을 찾아가는 여정",
            "세대 간의 갈등과 화해",
            "예기치 않은 만남이 바꾸는 인생",
            "과거와 현재가 교차하는 순간"
        ],
        "극": [
            "카페에서 벌어지는 우연한 만남",
            "가족 간의 비밀이 밝혀지는 순간",
            "직장에서의 갈등과 해결",
            "청춘들의 꿈과 현실",
            "사회적 편견에 맞서는 용기"
        ],
        "교술": [
            "현대인의 스마트폰 중독에 대하여",
            "환경 보호의 중요성",
            "독서의 가치와 의미",
            "AI 시대의 창의성",
            "소통의 부재와 그 해결책"
        ]
    }
    return random.choice(prompts.get(genre, ["자유 주제"]))

# 함수명을 export_to_text로 변경
def export_to_text(work_data: Dict) -> bytes:
    text_content = f"""
한국 현대 문학 창작 스튜디오
===========================

갈래: {work_data['genre']}
생성일: {work_data['timestamp']}
스타일: {work_data['style']}
길이: {work_data['length']}

작품:
{work_data['content']}

창작 과정:
"""
    for i, (q, a) in enumerate(zip(questions[work_data['genre']]["questions"], work_data['answers'])):
        text_content += f"\n{i+1}. {q}\n   답변: {a}\n"
    
    return text_content.encode('utf-8')

def display_sidebar():
    with st.sidebar:
        st.header("📚 창작 스튜디오")
        st.markdown("---")
        
        st.subheader("작품 히스토리")
        if st.session_state.works_history:
            for idx, work in enumerate(reversed(st.session_state.works_history[-5:])):
                with st.expander(f"{work['genre']} - {work['timestamp']}", expanded=False):
                    st.write(work['preview'][:100] + "...")
                    if st.button(f"전체 보기", key=f"view_{idx}"):
                        st.session_state.current_work = work
        else:
            st.info("아직 생성된 작품이 없습니다.")
        
        st.markdown("---")
        st.subheader("💡 창작 팁")
        tips = {
            "서정": "구체적인 이미지와 감각적 표현을 활용하세요.",
            "서사": "인물의 내면 갈등과 성장을 고려하세요.",
            "극": "대사를 통해 인물의 성격을 드러내세요.",
            "교술": "명확한 논지와 논거를 준비하세요."
        }
        for genre, tip in tips.items():
            st.markdown(f"**{genre}**: {tip}")
        
        st.markdown("---")
        st.subheader("📝 오늘의 글감")
        if st.button("🎲 랜덤 글감 받기"):
            random_genre = st.selectbox("갈래 선택", list(questions.keys()))
            prompt = get_writing_prompt(random_genre)
            st.info(f"💭 {prompt}")

def main():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.2);
    }
    .genre-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #E9ECEF;
        margin: 1rem 0;
        transition: all 0.3s;
    }
    .genre-card:hover {
        border-color: #FF6B6B;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    display_sidebar()
    
    st.title("🎨 한국 현대 문학 창작 스튜디오")
    st.markdown("### AI와 함께하는 창의적인 문학 여정")
    
    tab1, tab2, tab3 = st.tabs(["✍️ 새 작품 창작", "📖 작품 보기", "🔍 작품 분석"])
    
    with tab1:
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        genre_cols = {"서정": col1, "서사": col2, "극": col3, "교술": col4}
        
        selected_genre = None
        for genre, col in genre_cols.items():
            with col:
                st.markdown(f"""
                <div class="genre-card">
                    <h3 style="text-align: center;">{questions[genre]["icon"]}</h3>
                    <h4 style="text-align: center;">{genre}</h4>
                    <p style="text-align: center; font-size: 0.9rem; color: #6C757D;">
                        {questions[genre]["description"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"{genre} 선택", key=f"btn_{genre}", use_container_width=True):
                    selected_genre = genre
        
        if 'selected_genre' not in st.session_state:
            st.session_state.selected_genre = None
        
        if selected_genre:
            st.session_state.selected_genre = selected_genre
            st.session_state.show_generated_work = False  # 새 장르 선택시 이전 작품 숨기기
        
        if st.session_state.selected_genre:
            genre = st.session_state.selected_genre
            st.markdown(f"### {questions[genre]['icon']} {genre} 창작하기")
            
            with st.form(key="work_form"):
                answers = []
                for i, question in enumerate(questions[genre]["questions"]):
                    answer = st.text_area(
                        question, 
                        height=100,
                        key=f"q_{i}",
                        help="구체적이고 상세하게 답변할수록 더 풍부한 작품이 만들어집니다."
                    )
                    answers.append(answer)
                
                col1, col2 = st.columns(2)
                with col1:
                    style = st.selectbox(
                        "작품 스타일",
                        ["현대적", "고전적", "실험적", "미니멀리즘", "맥시멀리즘"],
                        help="작품의 전체적인 문체와 분위기를 결정합니다."
                    )
                with col2:
                    length = st.selectbox(
                        "작품 길이",
                        ["단편", "중편", "장편"],
                        help="생성될 작품의 분량을 선택합니다."
                    )
                
                submitted = st.form_submit_button("🎨 작품 생성하기", use_container_width=True)
                
                if submitted:
                    if all(answers):
                        with st.spinner('✨ 창작의 영감을 불어넣고 있습니다...'):
                            work = generate_work(genre, answers, style, length)
                            
                            work_data = {
                                "genre": genre,
                                "content": work,
                                "answers": answers,
                                "style": style,
                                "length": length,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "preview": work[:200]
                            }
                            st.session_state.works_history.append(work_data)
                            st.session_state.current_work = work_data
                            st.session_state.show_generated_work = True
                        
                        st.success("✅ 작품이 완성되었습니다!")
                        st.balloons()
                    else:
                        st.warning("⚠️ 모든 질문에 답변해주세요.")
            
            # 폼 외부에서 생성된 작품 표시 및 다운로드 버튼
            if hasattr(st.session_state, 'show_generated_work') and st.session_state.show_generated_work:
                work_data = st.session_state.current_work
                with st.expander("📜 생성된 작품 보기", expanded=True):
                    st.markdown(f"### {work_data['genre']} 작품")
                    st.write(work_data['content'])
                    
                    st.download_button(
                        label="📥 작품 다운로드",
                        data=work_data['content'],
                        file_name=f"{work_data['genre']}_작품_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        key="download_generated_work"
                    )
    
    with tab2:
        if st.session_state.current_work:
            work = st.session_state.current_work
            st.markdown(f"### {work['genre']} 작품")
            st.markdown(f"*생성 시간: {work['timestamp']}*")
            st.markdown(f"*스타일: {work['style']} | 길이: {work['length']}*")
            st.markdown("---")
            st.write(work['content'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 작품 다운로드",
                    data=work['content'],
                    file_name=f"{work['genre']}_작품_{work['timestamp'].replace(':', '-')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("📚 아직 선택된 작품이 없습니다. 새 작품을 창작하거나 사이드바에서 작품을 선택해주세요.")
    
    with tab3:
        if st.session_state.works_history:
            st.markdown("### 🔍 작품 분석하기")
            
            work_options = [f"{w['genre']} - {w['timestamp']}" for w in st.session_state.works_history]
            selected_work_idx = st.selectbox("분석할 작품 선택", range(len(work_options)), format_func=lambda x: work_options[x])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔬 작품 분석", use_container_width=True):
                    selected_work = st.session_state.works_history[selected_work_idx]
                    with st.spinner("🤔 작품을 분석하고 있습니다..."):
                        analysis = analyze_work(selected_work['content'], selected_work['genre'])
                    
                    st.markdown("### 📊 분석 결과")
                    st.write(analysis)
            
            with col2:
                # 버튼 텍스트와 기능 수정
                if st.button("📄 텍스트로 내보내기", use_container_width=True):
                    selected_work = st.session_state.works_history[selected_work_idx]
                    text_data = export_to_text(selected_work)
                    st.download_button(
                        label="📥 텍스트 다운로드",
                        data=text_data,
                        file_name=f"{selected_work['genre']}_작품_분석_{selected_work['timestamp'].replace(':', '-')}.txt",
                        mime="text/plain"
                    )
        else:
            st.info("📚 분석할 작품이 없습니다. 먼저 작품을 창작해주세요.")

if __name__ == "__main__":
    main()
