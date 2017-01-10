# *Created by zxiaobai on 17/1/9.
import yagmail
from routes import *

main = Blueprint('mail', __name__)


@async
def send_email(subject, user, recipient, check_code):
    yag = yagmail.SMTP(user=user, password='treenewbee225.cc', host='smtp.sina.com', port='25')
    body = check_code
    yag.send(to=recipient, subject=subject, contents=[body])
    print("成功发送邮件")


@main.route('/send', methods=['POST'])
def send_mail():
    subject, user, check_code = sent_email_config()
    form = request.form
    recipient = form['email']
    u = User.query.filter_by(email=form['email']).first()
    if u is None:
        u = User(form)
        u.code = check_code
        u.save()
        msg = '验证码已发送至邮箱'
        send_email(subject, user, recipient, check_code)
        return api_response(True, message=msg)
    if u.password != '':
        msg = '该邮箱已被注册'
        return api_response(message=msg)
    u.code = check_code
    u.email = form['email']
    u.save()
    send_email(subject, user, recipient, check_code)
    msg = '验证码已发送至邮箱'
    return api_response(True, message=msg)

