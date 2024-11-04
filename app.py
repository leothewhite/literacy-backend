from flask import Flask, request, jsonify
from summary import text_extraction, structure, find_word, explain
from tts import tts
import os
import base64

app = Flask(__name__)

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# 텍스트 추출
@app.route('/api/literacy-extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = "request.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)
    
    text = text_extraction() # 추출하는 함수 (summary.py)
    
    return jsonify({
        "text": text
    }), 200

# 핵심기능 수행
@app.route('/api/literacy-main', methods=['POST'])
def structure_text():
    data = request.get_json()

    mode = data.get('mode')

    if mode == 'structure':
        structured = structure(data.get('text'), data.get('level')) # 원문과 요약의 정도를 불러와서 구조화(요약)을 수행하는 함수
        return jsonify({
            'structure': structured
        }), 200

    if mode == 'word':
        word = find_word(data.get('text'))
        return jsonify({
            'word': word
        }), 200

    if mode == 'explain':
        exp = explain(data.get('text'))
        return jsonify({
            'explain': exp
        }), 200

# tts
@app.route('/api/literacy-tts', methods=['POST'])
def get_tts():
    data = request.get_json()

    ttss = base64.b64encode(tts(data.get('text'))).decode('utf8')

    return jsonify({
        'tts': ttss
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8765, debug=True)
