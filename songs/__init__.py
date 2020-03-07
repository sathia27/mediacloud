import os
from flask import Blueprint, Flask, render_template, request, redirect, jsonify, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/development.db'
app.secret_key = 'asdas2jmmasasdm9492744snfdaaddnasnandsasn'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ROOT_PATH = app.root_path


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    album = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(150), nullable=False)


db.create_all()


@app.route('/songs')
def index():
    return render_template('songs/index.html', songs=Song.query.all())


@app.route('/songs/new')
def new():
    return render_template('songs/new.html')


@app.route('/songs/download/<id>')
def download(id):
    song = Song.query.filter_by(id=id).first()
    file_path = ROOT_PATH + os.path.join(app.config['UPLOAD_FOLDER'], file_name(song))
    return send_file(file_path, attachment_filename=song.filename, as_attachment=True)


@app.route('/songs', methods=['POST'])
def create():
    file = request.files['file']
    if file and allowed_file(file.filename):
        data = request.form
        filename = secure_filename(file.filename)
        song = Song(name=data['name'], album=data['album'], filename=filename)
        db.session.add(song)
        db.session.commit()
        file.save(ROOT_PATH + os.path.join(app.config['UPLOAD_FOLDER'], file_name(song)))
    else:
        flash('File not present or Invalid file')
    return redirect(request.url)


def file_name(song):
    return str(song.id) + "_" + song.filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
