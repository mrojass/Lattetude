from slugify import slugify

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebook_id = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, facebook_id, name):
        self.facebook_id = facebook_id
        self.name = name
        self.username = slugify(name)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='author')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='post')


class Meetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)