from functools import wraps
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from flask import flash
from flask_mail import Mail, Message
from threading import Thread
import random
import uuid
import json
import os
import time
import requests
from models.user import User
from conf import *


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def current_user_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        user = current_user()
        if user is None:
            return redirect(url_for('user.login_view'))
        return f(user, *args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        user = current_user()
        if user is None:
            abort(404)
        if user.admin != 'true':
            user.unsafe += 1
            user.save()
            abort(404)
        return f(user, *args, **kwargs)

    return function


def api_response(status=False, data=None, message=None):
    r = dict(success=status,
             data=data,
             message=message)
    return json.dumps(r, ensure_ascii=False)


# 异步进程
def async(f):
    @wraps(f)
    def function(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return function


# 获取UC奇趣百科 json 数据
def get_max_pos():
    t = time.time()
    t = str(t)
    t = t[:10] + t[11:14]
    return t


def get_content(url, max_pos):
    content = requests.get(url + '&_max_pos=' + max_pos).content.decode()
    return json.loads(content)
