POSTGRESQL = 'postgresql+psycopg2://postgres:12345@localhost/blogpost_db'


class Config:
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    CKEDITOR_PKG_TYPE = 'basic'
