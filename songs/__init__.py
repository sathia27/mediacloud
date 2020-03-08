import os
from flask import Blueprint, Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.secret_key = 'asdas2jmmasasdm9492744snfdaaddnasnandsasn'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/development.db'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['UPLOAD_FOLDER'] = '/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp3'}
    app.url_map.strict_slashes = False
    os.makedirs(app.root_path + app.config.get('UPLOAD_FOLDER'), exist_ok=True)
    db.init_app(app)

    from .routes import song_blueprint
    app.register_blueprint(song_blueprint)

    with app.app_context():
        db.create_all()
        @app.route("/")
        def index():
           return render_template("index.html")
        return app