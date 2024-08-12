import openai

f = open('./res.txt', 'r')

result = f.read()

key_file = open('./keys/gpt_api_key.txt', 'r')

# OpenAI API 키 설정
openai.api_key = key_file.read()

# 메시지를 보내고 응답을 받는 함수 정의
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 사용할 모델 지정
        messages=[
            {"role": "system", "content": "너는 문해력이 낮은 요즘 학생들을 위해서 글을 요약해줘야 해. 내가 주는 입력을 요약해줘. 부가적인 설명과 잡다한 대답 없이 요약한 결과만 출력해줘."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

gpt_response = chat_with_gpt(result)

print(gpt_response)