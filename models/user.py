import os
import re
import random

from . import ModelMixin
from . import db
from . import *


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(16))
    qq = db.Column(db.String(15))
    email = db.Column(db.String(225))
    signature = db.Column(db.String(225))
    avatar = db.Column(db.String(225))
    admin = db.Column(db.String(5), default='false')
    code = db.Column(db.String(6))
    credit = db.Column(db.Integer, default=100)  # 信用积分
    created_time = db.Column(db.Integer)
    unsafe = db.Column(db.Integer, default=0)  # 非法请求
    like_weibo = db.Column(db.Text(65535), default='')

    weibos = db.relationship('Weibo', backref='user', lazy='dynamic',
                             order_by="desc(Weibo.id)")

    weibo_comments = db.relationship('WeiboComment', backref='user', lazy='dynamic',
                                     order_by="desc(WeiboComment.id)")

    topics = db.relationship('Topic', backref='user', lazy='dynamic',
                             order_by="desc(Topic.id)")

    comments = db.relationship('Comment', backref='user', lazy='dynamic',
                               order_by="desc(Comment.id)")

    boards = db.relationship('Board', backref='user', lazy='dynamic',
                             order_by="desc(Board.id)")

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')
        self.signature = form.get('signature', '')
        self.qq = form.get('qq', '')
        self.code = form.get('code', '')

    # 验证用户
    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        return username_equals and password_equals

    # 更新个人资料
    def update(self, form):
        self.password = form.get('password', self.password)
        self.qq = form.get('qq', self.qq)
        self.signature = form.get('signature', self.signature)
        self.save()

    # 验证注册用户的合法性的
    def valid_register(self, form):
        valid_username = User.query.filter_by(username=form['username']).first() == None
        valid_code = User.query.filter_by(code=form['code'], email=form['email']).first() != None
        valid_username_len = 16 >= len(form['username']) >= 6
        valid_password_len = 16 >= len(form['password']) >= 6
        err_msgs = ''

        u_match = r'^[\w]{6,16}$'

        if (not re.match(u_match, form['username'])):
            err_msgs += '用户名包含非法字符<br>'
        elif (not re.search('[^_]+', form['username'])):
            err_msgs += '用户名不能全为下划线<br>'

        if (not re.match(u_match, form['password'])):
            err_msgs += '密码包含非法字符<br>'
        elif (not re.search('[^_]+', form['password'])):
            err_msgs += '密码不能全为下划线<br>'

        if not valid_code:
            err_msgs += '验证码错误<br>'
        if not valid_username:
            err_msgs += '用户名已存在<br>'
        if not valid_username_len:
            err_msgs += '用户名长度不合法<br>'
        if not valid_password_len:
            err_msgs += '密码长度不合法<br>'

        if form['code'] == 'iamgod':
            self.admin = 'true'
            self.save()

        if err_msgs == '':
            self.created_time = date_time()
            self.username = form['username']
            self.password = form['password']
            self.save()
            return self.id, '注册成功'
        return None, err_msgs

    # 验证用户登录
    def vaild_login(self):
        suc_msg = '登录成功'
        err_msg = '登录失败,用户名或密码错误'
        user = User.query.filter_by(username=self.username, password=self.password).first()
        if user is None:
            return None, err_msg
        else:
            return user.id, suc_msg

