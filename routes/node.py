from routes import *

from models.node import Node

main = Blueprint('node', __name__)


@main.route('/')
@current_user_required
def index(user):
    return render_template('index.html', user=user)

