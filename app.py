from flask import Flask, request, jsonify, send_file
from summary import summary, text_extraction, oneLine, meaning
import os

app = Flask(__name__)

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# 이미지를 받아오고 요약 등의 기능을 수행하는 함수
@app.route('/api/literacy', methods=['POST'])
def summary_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    # 클라이언트에서 이미지 파일을 받아온 후 ./uploads/response.jpg 에 저장
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = "response.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)
    
    # 텍스트 추출, 요약, 단어 풀이 등의 기능 수행 후 json 형식으로 반환
    text = text_extraction()

    summed = summary(text)
    oneline = oneLine(summed)
    mean = meaning(text)

    return jsonify({"summary": summed, "original": text, "oneline": oneline, "meaning": mean}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8765, debug=True)
