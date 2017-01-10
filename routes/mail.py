# *Created by zxiaobai on 17/1/9.

from routes import *
from flask import Flask

app = Flask(__name__)

main = Blueprint('mail', __name__)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.sina.com',
    MAIL_PROT=465,
    MAIL_USERNAME='treenewbee225@sina.com',
    MAIL_PASSWORD='treenewbee225.cc',
    MAIL_DEBUG=True,
    MAIL_USE_TLS=True
)

mail = Mail(app)


@async
def send_async_email(app, msg):
    print('send_async_email')
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body):
    print('send_email')
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    send_async_email(app, msg)


@main.route('/send', methods=['POST'])
def send_mail():
    subject, sender, recipients, check_code, text_body = sent_email_config()
    form = request.form
    recipients.append(form['email'])
    u = User.query.filter_by(email=form['email']).first()
    if u is None:
        u = User(form)
        u.code = check_code
        u.save()
        msg = '验证码已发送至邮箱'
        print('success')
        send_email(subject, sender, recipients, text_body)
        return api_response(True, message=msg)
    if u.password != '':
        msg = '该邮箱已被注册'
        return api_response(message=msg)
    u.code = check_code
    u.email = form['email']
    u.save()
    msg = '验证码已发送至邮箱'
    return api_response(True, message=msg)

