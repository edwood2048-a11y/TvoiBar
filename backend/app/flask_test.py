from flask import Flask, request, jsonify
import os
import shutil

app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Go Buhat API'}

@app.route('/api/v1/users/<int:telegram_id>/upload-photo', methods=['POST'])
def upload_photo(telegram_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    upload_dir = "uploads/photos"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{telegram_id}_{file.filename}"
    file.save(file_path)
    
    photo_url = f"/uploads/photos/{telegram_id}_{file.filename}"
    
    return jsonify({'photo_url': photo_url})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002)