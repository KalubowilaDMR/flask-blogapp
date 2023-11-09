from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True, unique=True)
    email:Mapped[str] = mapped_column(db.String(150), unique=True)
    username:Mapped[str] = mapped_column(db.String(150), unique=True)
    password:Mapped[str] = mapped_column(db.String(150))
    date_created = mapped_column(db.DateTime(timezone=True), default=func.now())
    post = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

class Post(db.Model):
    __tablename__ = 'post'
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True, unique=True)
    text:Mapped[str] = mapped_column(db.String(10000), nullable=False)
    author:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = mapped_column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

    def __init__(self, text, author):
        self.text = text
        self.author = author

class Comment(db.Model):
    __tablename__ = 'comment'
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True, unique=True)
    text:Mapped[str] = mapped_column(db.String(200), nullable=False)
    author:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = mapped_column(db.DateTime(timezone=True), default=func.now())
    post_id:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, text, author, post_id):
        self.text = text
        self.author = author
        self.post_id = post_id

class Like(db.Model):
    __tablename__ = 'like'
    id:Mapped[int] = mapped_column(db.Integer, primary_key=True, unique=True)
    date_created = mapped_column(db.DateTime(timezone=True), default=func.now())
    author:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)