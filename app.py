from flask import Flask, request, jsonify
from summary import text_extraction, structure
from tts import tts
import os
import base64

app = Flask(__name__)

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# 이미지를 받아오고 요약 등의 기능을 수행하는 함수
@app.route('/api/literacy-extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    # 클라이언트에서 이미지 파일을 받아온 후 ./uploads/request.jpg 에 저장
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = "request.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)
    
    # 텍스트 추출, 요약, 단어 풀이 등의 기능 수행 후 json 형식으로 반환
    text = text_extraction()
    
    return jsonify({
        "text": text
    }), 200

@app.route('/api/literacy-main', methods=['POST'])
def structure_text():
    data = request.get_json()


    structured = structure(data.get('text'), data.get('level'))

    return jsonify({
        'structure': structured
    }), 200

# 텍스트로부터 tts 생성
@app.route('/api/literacy-tts', methods=['POST'])
def get_tts():
    data = request.get_json()

    # tts 오디오 파일을 받아온 후 클라이언트 측으로 전송하기 위해 base64로 인코딩 후 utf8로 디코드
    structure_tts = base64.b64encode(tts(data.get('structure'))).decode('utf8')

    return jsonify({
        "structure": structure_tts
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8765, debug=True)
