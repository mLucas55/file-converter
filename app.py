import os
from flask import Flask, render_template, request, abort, flash, send_file
from werkzeug.utils import secure_filename
import ffmpeg

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.webp', '.avif']
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
        # save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(upload_path)

        # construct output file path
        output_path = os.path.basename(upload_path)
        output_path = os.path.splitext(output_path)[0]
        output_path = output_path + '.' + request.form["output-type"]
        output_path = os.path.join("static", "output", output_path)

        # transcode file
        stream = ffmpeg.input(upload_path)
        stream = ffmpeg.output(stream, output_path)
        ffmpeg.run(stream, quiet=True, overwrite_output=True)

    flash('Upload Successful!', 'success')
    return send_file(output_path, as_attachment=True)
