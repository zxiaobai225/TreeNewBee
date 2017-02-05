# *Created by zxiaobai on 17/1/11.
from routes import *

from models.user import User
from models.board import Board

main = Blueprint('board', __name__)


@main.route('')
@current_user_required
def board(user):
    b = Board.query.all()
    return render_template('board.html', user=user, board=b)


@main.route('/add', methods=['POST'])
@current_user_required
def new_msg(user):
    form = request.form
    status, data, message = Board(form).board_add(user)
    return api_response(status, data, message)
