from flask import render_template, request, redirect, flash, send_file, url_for, Blueprint, current_app
from .song import Song
from werkzeug.utils import secure_filename
import sqlalchemy

song_blueprint = Blueprint('song_blueprint', __name__, url_prefix="/songs")

@song_blueprint.route('/')
def index():
    return render_template('songs/index.html', songs=Song.query.all())

@song_blueprint.route('/new')
def new():
    return render_template('songs/new.html')

@song_blueprint.route('/download/<id>')
def download(id):
    song = Song.query.filter_by(id=id).first()
    return send_file(song.uploadable_path(), attachment_filename=song.filename, as_attachment=True)

@song_blueprint.route('/play/<id>')
def play(id):
    song = Song.query.filter_by(id=id).first()
    return render_template('songs/play.html', file_path=url_for('.download', id=id), song=song)

@song_blueprint.route('/', methods=['POST'])
def create():
    file = request.files['file']
    if file and Song.allowed_file(file.filename):
        data = request.form
        filename = secure_filename(file.filename)
        song = Song(name=data['name'], album=data['album'], filename=filename)
        try:
            song.save()
            file.save(song.uploadable_path())
        except sqlalchemy.exc.IntegrityError:
            flash('Song already exists!')
    else:
        flash('File not present or Invalid file')
    return redirect(request.url)