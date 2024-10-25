import uuid
import json
import time
import requests
import openai

key_file = open('./keys.txt')
keys = key_file.readlines()

def text_extraction():
    # 셋업 및 페이로드 설정
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
    # 페이로드 설정
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
                {"role": "system", "content": f"여기서 어려운 단어를 찾아서 의미를 플어줘. ㅁㅁ: ---- 식으로, 부가적인 설명 없이."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    gpt_response = use_gpt(text)

    return gpt_response