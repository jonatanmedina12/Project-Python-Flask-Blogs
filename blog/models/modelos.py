from blog import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    photo = db.Column(db.String(200))
    is_active = db.Column(db.Integer, default=1)
    created_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email, photo=None):
        self.username = username
        self.password = password
        self.email = email
        self.photo = photo

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    is_active = db.Column(db.Integer, default=1)
    created_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, author_id, url, title, info=None, content=None):
        self.author_id = author_id
        self.url = url
        self.title = title
        self.info = info
        self.content = content

    def __repr__(self):
        return f'<Post {self.title}>'
