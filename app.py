import os
from flask import Flask, Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 50 MB file size limit
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['mp4', 'avi', 'mkv', 'mov', 'webm', 'flv', 'mpeg', 'wmv', 'hevc', 'h264',
                                   'mp3', 'aac', 'wav', 'flac', 'ogg', 'wma', 'alac', 'opus', 'png', 'jpeg', 
                                   'gif', 'bmp', 'tiff', 'webp']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)