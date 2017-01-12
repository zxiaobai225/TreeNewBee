# *Created by zxiaobai on 17/1/12.
import flask
import redis
import time
import json
from models.user import User

from routes import *

main = Blueprint('chat', __name__)


red = redis.Redis(host='localhost')
print('redis', red)
chat_channel = 'chat'


def stream():
    '''
    监听 redis 广播并 sse 到客户端
    '''
    # 对每一个用户 创建一个[发布订阅]对象
    pubsub = red.pubsub()
    # 订阅广播频道
    pubsub.subscribe(chat_channel)
    # 监听订阅的广播
    for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            # 用 sse 返回给前端
            yield 'data: {}\n\n'.format(data)


def current_time():
    return int(time.time())


@main.route('/index')
@current_user_required
def index_view(user):
    return flask.render_template('chat.html', user=user)


@main.route('/subscribe')
def subscribe():
    return flask.Response(stream(), mimetype="text/event-stream")


@main.route('/add', methods=['POST'])
@current_user_required
def chat_add(user):
    msg = request.get_json()
    name = user.username
    avatar = user.avatar
    content = msg.get('content', '')
    channel = msg.get('channel', '')
    r = {
        'name': name,
        'content': content,
        'channel': channel,
        'created_time': current_time(),
        'avatar': avatar,
    }
    message = json.dumps(r, ensure_ascii=False)
    print('debug', message)
    # 用 redis 发布消息
    red.publish(chat_channel, message)
    return 'OK'
