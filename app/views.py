# views.py

from flask import render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from app import app
from whatsappy import get_all_lines, parse_lines_into_df, get_word_corpus, \
    corpus_to_txt

ALLOWED_EXTENSIONS = set(['txt', 'text'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return analyze_file(filename)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template("upload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/results/<filename>')
def analyze_file(filename):
    lines = get_all_lines(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    df = parse_lines_into_df(lines, log_type='iphone')
    corpus = get_word_corpus(df)
    corpus_to_txt(corpus, 'app/results/{}_corpus.txt'.format(filename))
    return send_from_directory('results', '{}_corpus.txt'.format(filename))
