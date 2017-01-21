# *Created by zxiaobai on 17/1/11.
from . import ModelMixin
from . import db
from . import *


class Board(db.Model, ModelMixin):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(225))
    avatar = db.Column(db.String(225), db.ForeignKey('users.avatar'))
    username = db.Column(db.String(16), db.ForeignKey('users.username'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get("content", '')
        self.created_time = date_time()

    def valid(self):
        return 101 > len(self.content) > 1

    def board_add(self, user):
        if self.valid():
            self.username = user.username
            self.avatar = user.avatar
            self.save()
            return True, {'content': self.content,
                          'username': self.username,
                          'created_time': self.created_time,
                          'avatar': self.avatar,
                          }, '留言成功'

        return False, None, '留言不得少于2个字符多于100个字符'
