from flask import Flask, request, jsonify, send_file
from summary import summary, text_extraction, oneLine, meaning
import os

app = Flask(__name__)

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/api/literacy', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = "response.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)
    
    text = text_extraction()

    summed = summary(text)
    oneline = oneLine(summed)
    mean = meaning(text)

    return jsonify({"summary": summed, "original": text, "oneline": oneline, "meaning": mean}), 200

@app.route('/uploads/a.jpg', methods=['GET'])
def get_image():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'a.jpg')
    return send_file(filepath, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8765, debug=True)
