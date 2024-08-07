import streamlit as st
import random

# 한국 현대 문학 이론을 반영한 질문 리스트
questions = [
    "작품의 주제는 무엇인가요? (예: 개인과 사회의 갈등, 근대화의 영향, 전쟁의 상처)",
    "어떤 서술 시점을 사용하고 싶나요? (1인칭, 3인칭 전지적, 3인칭 제한적)",
    "작품의 시대적 배경은 언제인가요? (예: 일제강점기, 한국전쟁, 산업화 시대, 현대)",
    "주인공의 성격을 어떻게 설정하고 싶나요? (예: 내향적, 외향적, 이상주의적, 현실주의적)",
    "작품에서 다루고 싶은 한국 현대 문학의 주요 모티프가 있나요? (예: 고향, 이산, 도시와 농촌의 대비)",
    "어떤 문체를 사용하고 싶나요? (예: 서정적, 객관적, 실험적, 구어체)",
    "작품에서 사용하고 싶은 상징이 있나요? (예: 나비, 까마귀, 항아리)",
    "작품의 결말을 어떻게 구상하고 있나요? (열린 결말, 비극적 결말, 희망적 결말)",
    "한국 현대 문학의 어떤 흐름을 반영하고 싶나요? (예: 리얼리즘, 모더니즘, 포스트모더니즘)",
    "작품에서 다루고 싶은 사회적 이슈가 있나요? (예: 계급 문제, 성 역할, 세대 갈등)"
]

def generate_story(answers):
    # 여기에 실제 이야기 생성 로직을 구현합니다.
    # 이 예제에서는 간단한 템플릿을 사용합니다.
    story = f"""
    {answers[3]}인 주인공은 {answers[2]}을 배경으로 한 이야기에서 {answers[0]}에 대해 고민합니다. 
    {answers[1]} 시점으로 서술되는 이 작품은 {answers[5]} 문체를 사용하여 {answers[4]}를 탐구합니다. 
    {answers[6]}을(를) 상징으로 사용하여 {answers[8]}의 특징을 보여주며, 
    {answers[9]}와(과) 같은 사회적 이슈를 다룹니다. 
    결국 이야기는 {answers[7]}로 마무리됩니다.
    """
    return story

def main():
    st.title("한국 현대 문학 작품 생성 봇")
    
    st.write("다음 질문들에 답해주세요. 그러면 당신만의 한국 현대 문학 작품을 생성해 드리겠습니다.")
    
    answers = []
    for question in questions:
        answer = st.text_input(question)
        answers.append(answer)
    
    if st.button("작품 생성하기"):
        if all(answers):
            story = generate_story(answers)
            st.write("생성된 작품:")
            st.write(story)
        else:
            st.warning("모든 질문에 답해주세요.")

if __name__ == "__main__":
    main()
