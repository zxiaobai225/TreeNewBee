# *Created by zxiaobai on 17/1/22.
from routes import *

from models.user import User
from models.weibo import Weibo, WeiboComment

main = Blueprint('weibo', __name__)


@main.route('')
@current_user_required
def index(user):
    items_per_page = 20
    page = request.args.get('page', 1, type=int)
    # desc按倒序  asc按正序
    w = Weibo.query.order_by(Weibo.id.desc()).paginate(page, items_per_page, False)
    return render_template('weibo.html', user=user, weibo=w)


@main.route('/add', methods=['POST'])
@current_user_required
def new_weibo(user):
    form = request.form
    status, data, message = Weibo(form).save_weibo(user)
    return api_response(status, data, message)


@main.route('/comment/add', methods=['POST'])
@current_user_required
def new_comment(user):
    form = request.form
    weibo = Weibo.query.get_or_404(form.get('weibo_id'))
    status, data, message = WeiboComment(form).save_comment(user, weibo)
    return api_response(status, data, message)


@main.route('/like/<int:id>')
@current_user_required
def like(user, id):
    w = Weibo.query.get_or_404(id)
    status, data, message = w.like(user)
    return api_response(status, data, message)

