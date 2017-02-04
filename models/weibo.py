# *Created by zxiaobai on 17/1/22.
from . import ModelMixin
from . import db
from . import date_time


class Weibo(db.Model, ModelMixin):
    __tablename__ = 'weibos'
    id = db.Column(db.Integer, primary_key=True)
    weibo = db.Column(db.String(225))
    created_time = db.Column(db.Integer)
    comments_num = db.Column(db.Integer, default=0)
    like_nums = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    weibo_comments = db.relationship('WeiboComment', backref='weibo', lazy='dynamic',
                                     order_by="desc(WeiboComment.id)")

    def __init__(self, form):
        self.weibo = form.get('weibo', '')
        self.created_time = date_time()

    def like(self, user):
        u_likes = user.like_weibo.split(';')
        if str(self.id) in u_likes:
            self.like_nums -= 1
            u_likes.remove(str(self.id))
            user.like_weibo = ';'.join(u_likes)
            user.save()
            return True, {'like_nums': self.like_nums}, '取消点赞'
        user.like_weibo += (str(self.id) + ';')
        self.like_nums += 1
        self.save()
        return True, {'like_nums': self.like_nums}, '点赞成功'

    def valid(self):
        w = self.weibo.strip()
        l = len(w)
        if l < 3:
            return False, '微博太短了，不能少于 3 个字符'
        elif l > 100:
            return False, '微博太长了，不能超过 100 个字符'
        return True, '发送成功'

    def save_weibo(self, user):
        status, msg = self.valid()
        if status:
            self.user = user
            self.save()
            data = self.response()
        else:
            data = None
        return status, data, msg

    def delete_weibo(self):
        for i in self.comments:
            i.delete()
        self.delete()
        data = self.response()
        status = True
        msg = '微博删除成功'
        return status, data, msg

    def response(self):
        return dict(
            id=self.id,
            weibo=self.weibo,
            username=self.user.username,
            created_time=self.created_time,
            avatar=self.user.avatar,
            comments_num=self.comments_num,
            user_id=self.user.id)


class WeiboComment(db.Model, ModelMixin):
    __tablename__ = 'weibo_comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(225))
    created_time = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weibo_id = db.Column(db.Integer, db.ForeignKey('weibos.id'))

    def __init__(self, form):
        self.comment = form.get('comment', '')
        self.weibo_id = form.get('weibo_id', '')
        self.created_time = date_time()

    def valid(self):
        c = self.comment.strip()
        l = len(c)
        if l < 1:
            return False, '评论太短了，不能少于 1 个字符'
        elif l > 50:
            return False, '评论太长了，不能超过 50 个字符'
        return True, '发表评论成功'

    def save_comment(self, user, weibo):
        status, msg = self.valid()
        if status:
            self.user = user
            self.weibo = weibo
            self.weibo.comments_num += 1
            self.save()
            data = self.response()
        else:
            data = None
        return status, data, msg

    def response(self):
        return dict(comment=self.comment,
                    username=self.user.username,
                    created_time=self.created_time,
                    avatar=self.user.avatar,
                    user_id=self.user.id)

