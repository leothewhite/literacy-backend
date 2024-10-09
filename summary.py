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

    request_json = {'images': [{'format': 'jpg',
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

def summary(result):
    # 페이로드 설정
    def use_gpt(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 문해력이 낮은 요즘 학생들을 위해서 글을 요약해줘야 해. 내가 주는 입력을 요약해줘. 부가적인 설명과 잡다한 대답 없이 요약한 결과만 출력해줘."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']

    gpt_response = use_gpt(result)

    return gpt_response

def oneLine(text):
    def use_gpt(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 문해력이 낮은 요즘 학생들을 위해서 글을 요약해줘야 해. 내가 입력할 글은 이미 요약된 글이고, 너는 그 글을 공백 포함 50자 내외로 다시 요약할거야. 부가적인 설명 없이 요약된 결과만 출력해줘."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    
    gpt_response = use_gpt(text)

    return gpt_response


def meaning(text):
    def use_gpt(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "내가 주는 글에서 한자어로 된 단어들을 찾아줘. 그리고 표준국어대사전(https://stdict.korean.go.kr/main/main.do)에서 그 의미를 찾아줘. 부가적인 설명을 필요 없으며 단어(한자): 의미 형태로 출력해줘. 또한 의미를 초등학생도 쉽게 이해할 수 있게 다음 줄에 풀어쓴 의미: 내용 형식으로 풀어써줘."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
        
    gpt_response = use_gpt(text)

    return gpt_response
