import os
from flask import Flask, request, redirect, url_for, make_response, jsonify, abort
from flask import render_template
from werkzeug.utils import secure_filename
from main import classify_portrait

UPLOAD_FOLDER = './portraits'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET'])
def hello():
    return render_template('client.html')

@app.route('/classification/portrait', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    print(request.form)
    print(request.files)
    if 'file' not in request.files:
        return make_response(jsonify({'error': 'Files attribute not in request.'}), 404)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return make_response(jsonify({'error': 'No file selected.'}), 404)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        predictions = classify_portrait(filepath)
        return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)