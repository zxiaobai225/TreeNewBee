# *Created by zxiaobai on 17/1/11.
from . import ModelMixin
from . import db
from . import *


class Board(db.Model, ModelMixin):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(225))
    username = db.Column(db.String(16), db.ForeignKey('users.username'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get("content", '')
        self.username = form.get("username", '')
        self.created_time = date_time()

    def valid(self):
        return len(self.content) > 2

    def board_add(self, user):
        if self.valid():
            self.username = user.username
            self.save()
            return True, {'content': self.content,
                          'username': self.username,
                          'created_time': self.created_time,
                          }, '留言成功'

        return False, None, '留言至少3个字符'

