import os
import uuid
import json
import requests
from flask import Flask, render_template, request, url_for, \
    send_from_directory

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


# helpers

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def generate_unique_filename(filename):
    return str(uuid.uuid4())[:8] + '.' + filename.rsplit('.', 1)[1]


def call_api(file_url):
    print(str(file_url))
    url = 'http://api.pyimagesearch.com/face_detection/smart_crop/'
    image = "http://www.pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"
    payload = {"url": image}
    r = requests.post(url, data=payload)
    return json.loads(r.text)


# routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = generate_unique_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template(
                'results.html',
                filename=filename,
                api=call_api(url_for('uploaded_file', filename=filename))
            )
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
