import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from csv_to_html import csv_html_converter


UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'csv_files')
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return '''Hello, welcome to my apps. Check out the following apps:<br/>
    <a href="/csv_to_html">csv_to_html</a>'''


@app.route('/csv_to_html', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            html = csv_html_converter(file)
            return '<a href="/csv_to_html">Go back</a><br />' + html
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''