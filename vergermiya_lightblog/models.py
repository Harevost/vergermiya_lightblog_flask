"""
Vergermiya lightblog - models.py
"""

from flask_sqlalchemy import SQLAlchemy
from vergermiya_lightblog.extensions import bcrypt

db = SQLAlchemy()
posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
                      db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))


class User(db.Model):
    """
    Model of Users
    """
    __tablename__ = "users"
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='users', lazy='dynamic')

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        return "<User '{0}'>".format(self.username)

    def set_password(self, password):
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Post(db.Model):
    """
    Model of Post
    """

    __tablename__ = "posts"
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    datetime = db.Column(db.DateTime)
    author_id = db.Column(db.String(45), db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='posts', lazy='dynamic')
    tags = db.relationship('Tag', secondary=posts_tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<Post '{0}'>".format(self.title)


class Comment(db.Model):
    """
    Model of comments
    """
    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    datetime = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Comment `{}`>'.format(self.name)


class Tag(db.Model):
    """
    Model of Tags
    """
    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Tag `{}`>".format(self.name)
