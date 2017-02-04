# *Created by zxiaobai on 17/1/11.
from . import ModelMixin
from . import db
from . import *


class Board(db.Model, ModelMixin):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(225))
    created_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get("content", '')
        self.created_time = date_time()

    def valid(self):
        return 101 > len(self.content) > 1

    def board_add(self, user):
        if self.valid():
            self.user_id = user.id
            self.save()
            return True, {'content': self.content,
                          'username': self.user.username,
                          'created_time': self.created_time,
                          'avatar': self.user.avatar,
                          'id': self.id,
                          }, '留言成功'

        return False, None, '留言不得少于2个字符多于100个字符'
