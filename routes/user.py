from routes import *

from models.user import User

main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect(url_for('node.index'))
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.vaild_login()
    if user_id is None:
        return api_response(message=msg)
    session['user_id'] = user_id
    return api_response(True, message=msg)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.query.filter_by(email=form['email']).first()
    user_id, msg = u.valid_register(form)
    if user_id is None:
        return api_response(False, message=msg)
    session['user_id'] = user_id
    return api_response(True, message=msg)


@main.route('/logout')
@current_user_required
def logout(user):
    session.pop('user_id')
    return redirect(url_for('node.index'))
