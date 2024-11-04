import uuid
import json
import time
import requests
import openai

key_file = open('./keys.txt')
keys = key_file.readlines()

def text_extraction():
    api_url = 'https://8hiktk5tv5.apigw.ntruss.com/custom/v1/33325/5c41bfa54bca338e50b0223ee042f32d6f43570af778c53d13991477b0784015/general'
    secret_key = keys[0][:-1]

    path = "./uploads/request.jpg"
    files = [('file', open(path,'rb'))]

    request_json = {
        'images': [{
            'format': 'jpg',
            'name': 'demo'
        }],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
            
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    
    headers = {
    'X-OCR-SECRET': secret_key,
    }
    
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()
    
    content = ''

    for field in result['images'][0]['fields']:
        text = field['inferText']
        content += f'{text} '

    print(result)
    print(content)

    return content

openai.api_key = keys[1]

def structure(result, level):
    def use_gpt(prompt):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"내가 제시해주는 글을 간략하게 구조화해줘. 한 눈에 들어올 수 있게 1. 2. 3. 형식으로. 부가적인 설명 없이 결과값만을 줘. 간략한 정도를 1~10이라고 한다면 {level}만큼의 정도로 간략하게 해줘."
                    
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    gpt_response = use_gpt(result)

    return gpt_response


def find_word(text):
    def use_gpt(prompt):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"내가 주는 글에서 어려운 단어의 의미를 찾아줘. 부가적인 설명을 필요 없으며 단어: 의미 형태로 출력해줘. 또한 의미를 초등학생도 쉽게 이해할 수 있게 다음 줄에 풀어쓴 의미: 내용 형식으로 풀어써줘."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    gpt_response = use_gpt(text)

    return gpt_response


def explain(text):
    def use_gpt(prompt):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"이 글을 쉽게 풀어서 써줘. 문체는 유지하되 초등학생도 쉽게 이해할 수 있을 정도로."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    gpt_response = use_gpt(text)

    return gpt_response
