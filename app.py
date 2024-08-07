import os
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 문학 갈래별 질문 리스트
questions = {
    "서정": [
        "어떤 감정이나 정서를 표현하고 싶나요?",
        "시의 주제는 무엇인가요? (예: 사랑, 자연, 삶과 죽음)",
        "어떤 이미지나 비유를 사용하고 싶나요?",
        "시의 형식은 어떤 것을 선호하나요? (자유시, 정형시)",
        "어떤 분위기를 만들고 싶나요? (서정적, 우울한, 역동적 등)"
    ],
    "서사": [
        "이야기의 주요 플롯은 무엇인가요?",
        "주인공의 성격을 어떻게 설정하고 싶나요?",
        "작품의 시대적 배경은 언제인가요?",
        "어떤 문체를 사용하고 싶나요? (1인칭, 3인칭 등)",
        "작품에서 다루고 싶은 주요 주제나 메시지가 있나요?"
    ],
    "극": [
        "극의 주요 갈등은 무엇인가요?",
        "주요 등장인물들을 어떻게 설정하고 싶나요?",
        "극의 배경 (시간과 장소)은 어디인가요?",
        "어떤 종류의 극을 쓰고 싶나요? (비극, 희극, 풍자극 등)",
        "관객에게 전달하고 싶은 메시지는 무엇인가요?"
    ],
    "교술": [
        "어떤 주제나 개념을 설명하고 싶나요?",
        "목표로 하는 독자층은 누구인가요?",
        "어떤 형식을 사용하고 싶나요? (에세이, 논문, 평론 등)",
        "주장을 뒷받침할 주요 논거나 예시가 있나요?",
        "글의 톤은 어떻게 설정하고 싶나요? (학술적, 대중적, 비판적 등)"
    ]
}

def generate_work(genre, answers):
    prompt = f"""
    다음 정보를 바탕으로 한국 현대 문학의 {genre} 갈래에 해당하는 작품의 개요나 일부를 작성해주세요:

    1. {questions[genre][0]}: {answers[0]}
    2. {questions[genre][1]}: {answers[1]}
    3. {questions[genre][2]}: {answers[2]}
    4. {questions[genre][3]}: {answers[3]}
    5. {questions[genre][4]}: {answers[4]}

    이 정보를 바탕으로 300-500자 정도의 {genre} 작품 개요나 일부를 작성해주세요. 
    한국 현대 문학의 특징과 {genre} 갈래의 특성을 잘 반영하도록 해주세요.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"당신은 한국 현대 문학의 {genre} 갈래에 정통한 작가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def main():
    st.title("한국 현대 문학 작품 생성 봇")
    
    st.write("원하는 문학 갈래를 선택하고 질문에 답해주세요. 그러면 당신만의 한국 현대 문학 작품을 생성해 드리겠습니다.")
    
    genre = st.selectbox("문학 갈래를 선택하세요", ["서정", "서사", "극", "교술"])
    
    answers = []
    for question in questions[genre]:
        answer = st.text_input(question)
        answers.append(answer)
    
    if st.button("작품 생성하기"):
        if all(answers):
            with st.spinner('작품을 생성 중입니다...'):
                work = generate_work(genre, answers)
            st.write(f"생성된 {genre} 작품:")
            st.write(work)
        else:
            st.warning("모든 질문에 답해주세요.")

if __name__ == "__main__":
    main()
