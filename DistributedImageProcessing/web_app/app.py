from flask import Flask, render_template, request, send_from_directory
import os
from master_node import master

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_image():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return 'No file uploaded!', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file!', 400

    # Save uploaded image
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the image through the distributed system
    final_image = master.distribute_and_process(file_path)

    # Save processed image in results folder
    result_path = os.path.join(RESULT_FOLDER, 'processed_' + file.filename)
    final_image.save(result_path)

    return send_from_directory(RESULT_FOLDER, 'processed_' + file.filename)

if __name__ == "__main__":
    app.run(debug=True)
