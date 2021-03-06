import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Markup
from werkzeug.utils import secure_filename
from csv_to_html import csv_html_converter
from flask_sslify import SSLify


UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'csv_files')
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx'])

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file
app.config.update({'UPLOAD_FOLDER': UPLOAD_FOLDER, 'debug': False})
sslify = SSLify(app, permanent=True)
app.config.from_envvar('APP_SETTINGS', silent=True) # In case, it's needed


def allowed_file(filename):
    """
    Check for allowed extensions on the file - csv, xls, and xlsx
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/csv_to_html', methods=['GET', 'POST'])
def csv_bootstrap_table():
    """
    Function to upload a file and convert it to a responsive bootstrap table
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            html_text = csv_html_converter(file)
            html = Markup(html_text)
            return render_template('bootstrap_table.html', html=html, html_code=html_text)
    return render_template('form.html')


@app.route('/track_ga_urls', methods=['GET', 'POST'])
def url_event_listener():
    """
    Modify a list of urls to track with Google analytics
    """
    track_template = "<a href=\"{0}\" target=\"_blank\" onclick=\"trackOutboundLink('{0}'); return false;\""
    if request.method == 'POST':
        urls = request.form['url_textbox']
        track_urls = [track_template.format(url.strip()) for url in urls.split('\n')]
        return render_template('link_tracking.html', links=track_urls)
    return render_template('link_tracking.html', links=[])