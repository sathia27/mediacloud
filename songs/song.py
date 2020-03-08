from . import db
import os
from flask import current_app as app


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    album = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()



    def uploadable_path(self):
        return app.root_path + os.path.join(app.config['UPLOAD_FOLDER'], self.file_name())

    def file_name(self):
        return str(self.id) + "_" + self.filename

    @classmethod
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config.get('ALLOWED_EXTENSIONS')