from routes import *

from models.user import User

main = Blueprint('user', __name__)


@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect(url_for('qiqu.index'))
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    user_id, msg = u.vaild_login()
    if user_id is None:
        return api_response(message=msg)
    session.permanent = True
    session['user_id'] = user_id
    return api_response(True, message=msg)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User(form)
    user_id, msgs = u.valid_register()
    if user_id is None:
        return api_response(message=msgs)
    u.avatar = 'avatar%s.jpeg' % ''.join([str(i) for i in random.sample(range(0, 9), 1)])
    u.save()
    session.permanent = True
    session['user_id'] = u.id
    return api_response(True)


@main.route('/logout')
@current_user_required
def logout(user):
    session.pop('user_id')
    return redirect(url_for('qiqu.index'))


@main.route('/profile/<username>')
@current_user_required
def profile(user, username):
    othuser = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user, othuser=othuser)


@main.route('/qeertyuiopasdf')
@current_user_required
def all_user(user):
    if user.admin != 'true':
        user.unsafe += 1
        user.save()
        abort(404)
    au = User.query.all()
    return render_template('alluser.html', user=user, all_user=au)
