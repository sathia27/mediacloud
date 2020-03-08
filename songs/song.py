from . import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    album = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(150), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()