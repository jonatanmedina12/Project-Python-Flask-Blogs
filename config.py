import os

POSTGRESQL = 'postgresql+psycopg2://postgres:12345@localhost/blogpost_db'


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_PKG_TYPE = 'full'
    CKEDITOR_SERVE_LOCAL = True
    # Asegúrate de que CKEDITOR_HEIGHT esté configurado
    CKEDITOR_HEIGHT = 400  # Ajusta la altura según sea necesario
