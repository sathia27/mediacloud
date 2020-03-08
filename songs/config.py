class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/development.db'
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = {'mp3'}