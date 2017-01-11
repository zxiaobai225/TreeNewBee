# *Created by zxiaobai on 17/1/11.
from routes import *

from models.user import User

main = Blueprint('profile', __name__)


@main.route('/update', methods=['POST'])
@current_user_required
def update(user):
    form = request.form
    user.update(form)
    msg = '修改成功'
    return api_response(True, message=msg)
