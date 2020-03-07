from flask import render_template, request, redirect, flash, send_file, url_for, Blueprint, current_app
from .song import Song
from . import db
import os
from werkzeug.utils import secure_filename

song = Blueprint('song', __name__, url_prefix="/songs")

# ROOT_PATH = app.root_path

@song.route('/')
def index():
    return render_template('songs/index.html', songs=Song.query.all())

@song.route('/new')
def new():
    return render_template('songs/new.html')

@song.route('/download/<id>')
def download(id):
    song = Song.query.filter_by(id=id).first()
    file_path = current_app.root_path + os.path.join(current_app.config['UPLOAD_FOLDER'], file_name(song))
    return send_file(file_path, attachment_filename=song.filename, as_attachment=True)

@song.route('/play/<id>')
def play(id):
    return render_template('songs/play.html', file_path=url_for('.download', id=id))

@song.route('/', methods=['POST'])
def create():
    file = request.files['file']
    if file and allowed_file(file.filename):
        data = request.form
        filename = secure_filename(file.filename)
        song = Song(name=data['name'], album=data['album'], filename=filename)
        db.session.add(song)
        db.session.commit()
        file.save(current_app.root_path + os.path.join(current_app.config['UPLOAD_FOLDER'], file_name(song)))
    else:
        flash('File not present or Invalid file')
    return redirect(request.url)

def file_name(song):
    return str(song.id) + "_" + song.filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS')