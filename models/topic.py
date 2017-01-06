from . import ModelMixin
from . import db
from . import date_time


class Topic(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225))
    content = db.Column(db.String(225))
    created_time = db.Column(db.String(225), default=date_time())
    updated_time = db.Column(db.String(225), default=date_time())
    views = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))

    def __init__(self, form):
        print('topic init', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.board_id = form.get('board_id', 0)

    def update(self, form):
        print('topic update', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = date_time()
        self.save()


class Comment(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(225))
    created_time = db.Column(db.String(225), default=date_time())
    updated_time = db.Column(db.String(225), default=date_time())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __init__(self, form):
        print('comment init', form)
        self.content = form.get('content', '')
        self.topic_id = form.get('topic_id', '')
